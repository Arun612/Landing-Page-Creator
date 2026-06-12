"""
Core orchestrator — EnhancedLandingPageCreatorSystem.

Wires together agents, image services, templates, and the editor
to execute the 4-phase landing page generation pipeline:

  Phase 1  Strategy + Content  (parallel)
  Phase 2  Section design + Image acquisition  (parallel, 7 workers)
  Phase 3  HTML integration  (Integrator agent)
  Phase 4  Post-integration QA review  (Review agent)
"""

import json
import logging
import re
import time
# ThreadPoolExecutor removed — free-tier branch uses sequential execution
# to stay within Groq's 12K tokens/min rate limit.
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from openai import AzureOpenAI

from .agents import create_agents
from .business import enhance_business_context
from .config import Config
from .editor import LandingPageEditor
from .image_service import ImageService
from .llm import build_llm_setup, verify_llm
from .templates import create_fallback_html, get_theme_instructions

logger = logging.getLogger(__name__)


class EnhancedLandingPageCreatorSystem:
    """
    Orchestrates a multi-agent pipeline to generate production-ready
    HTML landing pages for any business type.
    """

    def __init__(self, config: Config):
        self._config = config

        # ── LLM client (Azure, Groq, or Ollama) ──────────────
        self._llm = build_llm_setup(config)

        dalle_client = None
        if config.dalle_deployment and config.llm_provider == "azure":
            dalle_client = AzureOpenAI(
                api_key=config.dalle_api_key or config.azure_openai_api_key,
                api_version=config.dalle_api_version,
                azure_endpoint=config.dalle_endpoint or config.azure_openai_endpoint,
            )

        # ── Sub-systems ──────────────────────────────────────
        self._agents = create_agents(self._llm.llm_config)
        self._image_service = ImageService(
            llm_setup=self._llm,
            dalle_client=dalle_client,
            dalle_deployment=config.dalle_deployment,
            pixabay_api_key=config.pixabay_api_key,
        )
        self.editor = LandingPageEditor(self._agents)

        # ── Verify deployments ───────────────────────────────
        self._verify_deployments()

    # ─── Deployment verification ─────────────────────────────

    def _verify_deployments(self) -> None:
        """Smoke-test each configured API endpoint."""
        try:
            verify_llm(self._llm)
        except Exception as exc:
            provider = self._config.llm_provider
            raise RuntimeError(
                f"❌ LLM provider '{provider}' (model '{self._llm.model}') failed: {exc}"
            ) from exc

        if self._config.dalle_deployment and self._config.llm_provider == "azure":
            try:
                dalle = AzureOpenAI(
                    api_key=self._config.dalle_api_key or self._config.azure_openai_api_key,
                    api_version=self._config.dalle_api_version,
                    azure_endpoint=self._config.dalle_endpoint or self._config.azure_openai_endpoint,
                )
                dalle.images.generate(
                    model=self._config.dalle_deployment,
                    prompt="A simple test image",
                    size="1024x1024",
                    n=1,
                )
                print(f"✅ DALL-E deployment '{self._config.dalle_deployment}' verified")
            except Exception as exc:
                print(f"⚠️  DALL-E test failed: {exc}")
        elif self._config.dalle_deployment:
            print("ℹ️  DALL-E skipped (requires LLM_PROVIDER=azure)")
        else:
            print("ℹ️  DALL-E not configured")

        if self._config.pixabay_api_key:
            try:
                self._image_service.fetch_pixabay_images("test", per_page=1)
                print("✅ Pixabay API verified")
            except Exception as exc:
                print(f"⚠️  Pixabay test failed: {exc}")
        else:
            print("ℹ️  Pixabay not configured")

    # ─── Agent runners ───────────────────────────────────────

    def _run_agent(self, agent_key: str, message: str) -> str:
        """Run a single agent and return its response content."""
        chat = self._agents["user_proxy"].initiate_chat(
            self._agents[agent_key],
            message=message,
            max_turns=1,
        )
        return chat.chat_history[-1]["content"]

    # ─── Main pipeline ───────────────────────────────────────

    def create_landing_page(
        self,
        business_info: Dict,
        image_choice: str = "both",
        user_image_url: Optional[str] = None,
        theme: str = "light",
    ) -> Dict:
        """
        Execute the full 4-phase generation pipeline.

        Returns a dict with ``success``, ``files``, ``sections``,
        ``metadata``, and timing information.
        """
        try:
            t0 = time.time()

            # Enrich with industry guidance
            enhanced = enhance_business_context(business_info)
            theme_instructions = get_theme_instructions(theme)

            # Output directory
            slug = re.sub(r"[^a-zA-Z0-9]", "_", enhanced["business_name"].lower())
            out_dir = Path("output") / slug
            out_dir.mkdir(parents=True, exist_ok=True)

            btype = enhanced.get("business_type", "General")
            guidance = enhanced["industry_guidance"]

            context = (
                f"BUSINESS INFORMATION:\n{json.dumps(enhanced, indent=2)}\n\n"
                f"INDUSTRY GUIDANCE:\n"
                f"Business Type: {btype}\n"
                f"Key Values: {guidance['key_values']}\n"
                f"Recommended Tone: {guidance['tone']}\n"
                f"Focus Areas: {guidance['focus_areas']}\n"
                f"Social Proof Type: {guidance['social_proof']}\n"
                f"Urgency Type: {guidance['urgency_type']}\n\n"
                f"THEME: {theme.upper()}\n{theme_instructions}\n\n"
                f"IMAGE CHOICE: {image_choice}\n\n"
                f"CRITICAL: This is a {btype} landing page. "
                f"Generate substantial, industry-appropriate content. "
                f"Minimum 200 words per agent response."
            )

            # ══ PHASE 1 — Strategy + Content (sequential for free-tier TPM limits) ══
            print("⚡ Phase 1: Strategy agent …")
            strategy_result = self._run_agent(
                "strategy",
                f"Develop a comprehensive landing page strategy:\n{context}",
            )
            time.sleep(5)  # cooldown — stay under Groq free-tier 12K TPM limit
            print("⚡ Phase 1: Content agent …")
            content_result = self._run_agent(
                "content",
                f"Create high-converting content:\n{context}",
            )
            time.sleep(5)

            # Retry if too short
            if len(strategy_result.strip()) < 100:
                print("  ↻ Strategy too short — retrying …")
                strategy_result = self._run_agent(
                    "strategy",
                    f"IMPORTANT: previous attempt was too short. Retry:\n{context}",
                )
            if len(content_result.strip()) < 100:
                print("  ↻ Content too short — retrying …")
                content_result = self._run_agent(
                    "content",
                    f"IMPORTANT: previous attempt was too short. Retry:\n{context}",
                )

            t1 = time.time()
            print(f"  ✓ Phase 1 done in {t1 - t0:.1f}s")

            enriched = (
                f"{context}\n\nSTRATEGY ANALYSIS:\n{strategy_result}\n\n"
                f"CONTENT FRAMEWORK:\n{content_result}"
            )

            # ══ PHASE 2 — Sections + Image (sequential for free-tier TPM limits) ══
            print("⚡ Phase 2: Section agents (sequential — free-tier mode) …")
            section_msgs = {
                "navbar":       f"Create navbar for {btype} {theme}-themed page with industry-appropriate navigation.",
                "hero":         f"Create hero section for {btype} {theme}-themed page. Focus on {guidance['key_values'][0]} and {guidance['key_values'][1]}.",
                "features":     f"Create features section for {btype} {theme}-themed page. Highlight {', '.join(guidance['focus_areas'])}.",
                "testimonials": f"Create testimonials for {btype} {theme}-themed page. Use {guidance['social_proof']} approach. USE BOOTSTRAP ICONS FOR AVATARS.",
                "cta":          f"Create CTA section for {btype} {theme}-themed page. Use {guidance['urgency_type']} urgency.",
                "footer":       f"Create footer for {btype} {theme}-themed page with appropriate contact info.",
            }

            sections = {}
            for name, msg in section_msgs.items():
                print(f"  → {name} …")
                result = self._run_agent(name, f"{msg}\n\n{enriched}")
                if len(result.strip()) < 50:
                    result = f"FALLBACK: Create {name} section for {btype} with Bootstrap icons and {theme} theme."
                sections[name] = result
                time.sleep(5)  # cooldown between agents

            print("  → image …")
            image_agent_response = self._run_agent(
                "image",
                f"Create image suggestions for {btype} with {theme} theme:\n{enriched}",
            )
            time.sleep(5)

            # Resolve hero image
            hero_url, img_source = self._image_service.get_hero_image(
                enhanced, image_choice, user_image_url,
                image_agent_response, theme,
            )

            t2 = time.time()
            print(f"  ✓ Phase 2 done in {t2 - t0:.1f}s")

            # Image context
            if hero_url:
                print(f"  🖼️  Hero image: {img_source}")
                enriched += f"\n\nHERO IMAGE URL: {hero_url}\nIMAGE SOURCE: {img_source}\nIMPORTANT: Use this exact URL in the hero section."
            else:
                print(f"  🖼️  No hero image ({img_source})")
                enriched += f"\n\nNO HERO IMAGE: Use {theme} theme gradient/pattern for hero background."

            # ══ PHASE 3 — Integration ════════════════════════
            print("⚡ Phase 3: Integrating into final HTML …")
            integration_ctx = (
                f"BUSINESS TYPE: {btype.upper()}\n"
                f"INDUSTRY REQUIREMENTS: {guidance}\n\n"
                f"THEME: {theme.upper()}\n{theme_instructions}\n\n"
                f"BUSINESS CONTEXT:\n{enriched}\n\n"
                f"HTML SECTIONS:\n"
                + "\n".join(f"{k.upper()}: {v}" for k, v in sections.items())
                + "\n\nINTEGRATION INSTRUCTIONS:\n"
                f"- Apply {btype} design elements and color schemes\n"
                f"- Tone: {guidance['tone']}\n"
                f"- Focus: {', '.join(guidance['focus_areas'])}\n"
                "- Minimum 2000 words total\n"
                "- NO placeholder content or empty sections\n"
                "- Generate complete, functional HTML.\n"
            )

            integration_chat = self._agents["user_proxy"].initiate_chat(
                self._agents["integrator"],
                message=f"Integrate all sections into a complete {btype} {theme}-themed landing page:\n{integration_ctx}",
                max_turns=1,
            )

            html = integration_chat.chat_history[-1]["content"]
            html = re.sub(r"^```html\n?", "", html)
            html = re.sub(r"\n?```", "", html)

            t3 = time.time()
            print(f"  ✓ Phase 3 done in {t3 - t0:.1f}s")

            # ══ PHASE 4 — Post-integration QA ════════════════
            print("⚡ Phase 4: QA review on assembled HTML …")
            review_msg = (
                f"Review this assembled HTML landing page for a {btype} business.\n"
                f"BUSINESS CONTEXT:\n{json.dumps(enhanced, indent=2)}\n\n"
                f"ASSEMBLED HTML:\n{html}"
            )
            review_chat = self._agents["user_proxy"].initiate_chat(
                self._agents["review"],
                message=review_msg,
                max_turns=1,
            )
            review_result = review_chat.chat_history[-1]["content"]

            # Extract corrected HTML if the reviewer provided fixes
            corrected_match = re.search(
                r"CORRECTED_HTML_START:\s*(.*?)\s*CORRECTED_HTML_END:",
                review_result, re.DOTALL | re.IGNORECASE,
            )
            if corrected_match:
                corrected = corrected_match.group(1).strip()
                if len(corrected) > 500:
                    html = corrected
                    print("  ✓ QA fixes applied")

            t4 = time.time()
            print(f"  ✓ Phase 4 done in {t4 - t0:.1f}s")

            # Fallback if HTML is too small
            if len(html.strip()) < 1000:
                print("  ⚠️  HTML too short — using fallback template")
                html = create_fallback_html(enhanced, theme, sections, hero_url)

            # ── Persist ──────────────────────────────────────
            self.editor.current_html = html
            self.editor.current_context = enriched

            html_file = out_dir / f"{slug}_{btype.lower()}_{theme}_landing_page.html"
            html_file.write_text(html, encoding="utf-8")

            total = time.time() - t0
            print(f"\n✅ Total generation time: {total:.1f}s")

            return {
                "success": True,
                "files": {"html_file": str(html_file)},
                "sections": list(sections.keys()),
                "metadata": {
                    "business_info": enhanced,
                    "business_type": btype,
                    "industry_guidance": guidance,
                    "theme": theme,
                    "image_choice": image_choice,
                    "image_source": img_source,
                    "hero_image_url": hero_url,
                    "sections_created": list(sections.keys()),
                    "created_at": datetime.now().isoformat(),
                    "editable": True,
                    "generation_time_seconds": total,
                    "performance": {
                        "phase1_strategy_content": round(t1 - t0, 1),
                        "phase2_sections_image": round(t2 - t1, 1),
                        "phase3_integration": round(t3 - t2, 1),
                        "phase4_qa_review": round(t4 - t3, 1),
                    },
                },
                "editing_available": True,
                "generation_time": total,
                "business_type": btype,
            }

        except Exception as exc:
            logger.error("Pipeline failed: %s", exc)
            return {"success": False, "error": str(exc)}

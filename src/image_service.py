"""
Image service — DALL-E 3 generation, Pixabay stock photos, and
LLM-based keyword extraction.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple

import requests
from openai import AzureOpenAI

logger = logging.getLogger(__name__)


class ImageService:
    """Handles all image acquisition for the landing page pipeline."""

    def __init__(
        self,
        gpt_client: AzureOpenAI,
        gpt_deployment: str,
        dalle_client: Optional[AzureOpenAI] = None,
        dalle_deployment: Optional[str] = None,
        pixabay_api_key: Optional[str] = None,
    ):
        self._gpt_client = gpt_client
        self._gpt_deployment = gpt_deployment
        self._dalle_client = dalle_client
        self._dalle_deployment = dalle_deployment
        self._pixabay_key = pixabay_api_key

    # ── DALL-E ───────────────────────────────────────────────────

    def generate_dalle_image(self, prompt: str, theme: str = "light") -> Optional[str]:
        """Generate an image with DALL-E 3 and return its URL."""
        if not self._dalle_client or not self._dalle_deployment:
            logger.info("DALL-E not configured — skipping.")
            return None

        enhancements = {
            "light": "bright professional lighting, clean white/light background, modern minimalist aesthetic, high quality, 4k",
            "dark":  "dramatic professional lighting, dark gradient background, high contrast, modern sleek aesthetic, premium quality, 4k",
        }
        enhanced = f"{prompt}, {enhancements.get(theme, enhancements['light'])}, professional photography style"
        enhanced = enhanced[:400]

        try:
            logger.info("Generating %s-themed image with DALL-E …", theme)
            response = self._dalle_client.images.generate(
                model=self._dalle_deployment,
                prompt=enhanced,
                size="1792x1024",
                n=1,
                quality="standard",
            )
            url = response.data[0].url
            logger.info("DALL-E image generated successfully.")
            return url
        except Exception as exc:
            logger.error("DALL-E generation failed: %s", exc)
            return None

    # ── Pixabay ──────────────────────────────────────────────────

    def fetch_pixabay_images(self, keywords, per_page: int = 5) -> List[Dict]:
        """Fetch professional stock photos from Pixabay."""
        if not self._pixabay_key:
            logger.info("Pixabay API key not configured.")
            return []

        if isinstance(keywords, str):
            query = keywords
        else:
            clean = [kw.strip().lower() for kw in keywords if kw.strip()]
            query = "+".join(clean[:3])

        logger.info("Searching Pixabay for: %s", query)

        params = {
            "key": self._pixabay_key,
            "q": query,
            "image_type": "photo",
            "orientation": "horizontal",
            "category": "business",
            "per_page": per_page,
            "safesearch": "true",
            "min_width": 1920,
            "min_height": 1080,
            "order": "popular",
            "editors_choice": "true",
        }

        try:
            resp = requests.get("https://pixabay.com/api/", params=params, timeout=10)
            if resp.status_code == 200:
                hits = resp.json().get("hits", [])
                logger.info("Pixabay returned %d images.", len(hits))
                return hits
            logger.error("Pixabay API error: %d — %s", resp.status_code, resp.text)
            return []
        except requests.RequestException as exc:
            logger.error("Pixabay request failed: %s", exc)
            return []

    # ── Keyword extraction ───────────────────────────────────────

    def extract_keywords_llm(self, text: str, num_keywords: int = 5) -> List[str]:
        """Use GPT to extract visual search keywords from business info."""
        prompt = (
            f"Extract the top {num_keywords} most relevant single-word keywords "
            f"from this business information for searching professional hero images "
            f"on Pixabay. Focus on visual concepts. Return comma-separated words only.\n\n"
            f"BUSINESS INFO:\n{text}"
        )
        try:
            resp = self._gpt_client.chat.completions.create(
                model=self._gpt_deployment,
                messages=[
                    {"role": "system", "content": "Extract concise keywords for professional image searches."},
                    {"role": "user", "content": prompt},
                ],
                max_completion_tokens=100,
                temperature=0,
            )
            return [kw.strip() for kw in resp.choices[0].message.content.split(",") if kw.strip()]
        except Exception as exc:
            logger.error("Keyword extraction failed: %s", exc)
            return ["business", "professional", "technology", "office", "modern"]

    # ── Orchestration ────────────────────────────────────────────

    def get_hero_image(
        self,
        business_info: Dict,
        image_choice: str,
        user_image_url: Optional[str],
        image_agent_response: str,
        theme: str = "light",
    ) -> Tuple[Optional[str], str]:
        """
        Acquire a hero image based on the user's preference.

        Parameters
        ----------
        image_agent_response : str
            Raw output from the Image Agent containing DALL-E prompts
            and Pixabay keywords.

        Returns
        -------
        (image_url, source_label)
        """
        if image_choice == "none":
            return None, "none"

        if image_choice == "user_url" and user_image_url:
            if user_image_url.startswith(("http://", "https://")):
                return user_image_url, "user_provided"
            logger.warning("Invalid URL format: %s", user_image_url)
            return None, "invalid_url"

        # Parse agent output
        dalle_prompt = None
        match = re.search(
            r"DALLE_PROMPT_START:\s*(.*?)\s*DALLE_PROMPT_END:",
            image_agent_response, re.DOTALL | re.IGNORECASE,
        )
        if match:
            dalle_prompt = match.group(1).strip()

        pixabay_keywords: List[str] = []
        match = re.search(
            r"PIXABAY_KEYWORDS_START:\s*(.*?)\s*PIXABAY_KEYWORDS_END:",
            image_agent_response, re.DOTALL | re.IGNORECASE,
        )
        if match:
            pixabay_keywords = [kw.strip() for kw in match.group(1).split(",") if kw.strip()]

        # ── Attempt acquisition based on user preference ─────────
        if image_choice in ("dalle", "both") and dalle_prompt:
            url = self.generate_dalle_image(dalle_prompt, theme)
            if url:
                return url, "dalle"

        if image_choice in ("pixabay", "both", "dalle") and pixabay_keywords:
            images = self.fetch_pixabay_images(pixabay_keywords)
            if images:
                return images[0]["webformatURL"], "pixabay"

        # ── Fallback: extract keywords from raw business info ────
        logger.info("Using fallback keyword extraction.")
        fallback = self.extract_keywords_llm(
            f"{business_info.get('business_name', '')} "
            f"{business_info.get('business_type', '')} "
            f"{business_info.get('description', '')}"
        )
        if fallback:
            images = self.fetch_pixabay_images(fallback)
            if images:
                return images[0]["webformatURL"], "pixabay_fallback"

        return None, "failed"

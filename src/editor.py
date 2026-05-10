"""
Interactive landing page editor.

Allows users to request iterative changes to an already-generated
landing page through a conversational loop powered by the Integrator agent.
"""

import os
import re
import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)


class LandingPageEditor:
    """Manages interactive editing sessions for generated landing pages."""

    def __init__(self, agents: dict):
        self._agents = agents
        self.current_html: str | None = None
        self.current_context: str | None = None

    def edit_landing_page(self, edit_request: str) -> Dict:
        """
        Apply a single edit request to the current HTML.

        Returns
        -------
        dict with keys ``success``, ``updated_html`` (on success),
        or ``error`` (on failure).
        """
        if not self.current_html or not self.current_context:
            return {"success": False, "error": "No landing page loaded. Create one first."}

        try:
            edit_context = (
                f"CURRENT HTML TO EDIT:\n{self.current_html}\n\n"
                f"ORIGINAL CONTEXT:\n{self.current_context}\n\n"
                f"USER EDIT REQUEST:\n{edit_request}\n\n"
                "EDITING INSTRUCTIONS:\n"
                "- Make the requested changes precisely\n"
                "- Maintain the overall structure and theme\n"
                "- Keep all CDN links and functionality intact\n"
                "- Maintain responsive design\n"
                "- Update only what was requested\n"
            )

            chat = self._agents["editing_proxy"].initiate_chat(
                self._agents["integrator"],
                message=f"Edit the landing page HTML based on this request:\n{edit_context}",
                max_turns=1,
            )

            updated = chat.chat_history[-1]["content"]
            updated = re.sub(r"^```html\n?", "", updated)
            updated = re.sub(r"\n?```", "", updated)

            self.current_html = updated
            logger.info("Landing page edited successfully.")

            return {
                "success": True,
                "updated_html": updated,
                "edit_request": edit_request,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as exc:
            logger.error("Error editing landing page: %s", exc)
            return {"success": False, "error": str(exc)}

    def start_interactive_editing(self, html_file_path: str) -> None:
        """Run an interactive editing loop reading/writing the given HTML file."""
        if not os.path.exists(html_file_path):
            print(f"❌ HTML file not found: {html_file_path}")
            return

        with open(html_file_path, "r", encoding="utf-8") as fh:
            self.current_html = fh.read()

        print("\n" + "=" * 60)
        print("🎨 INTERACTIVE LANDING PAGE EDITOR")
        print("=" * 60)
        print(f"✅ Loaded: {html_file_path}")
        print("\n📝 Commands:")
        print("  • Describe your change  →  apply it")
        print("  • 'preview'             →  show file path")
        print("  • 'save'                →  save current version")
        print("  • 'exit'                →  end session")
        print("-" * 60)

        max_edits = 10
        for edit_num in range(1, max_edits + 1):
            try:
                print(f"\n🔧 EDIT #{edit_num}/{max_edits}")
                user_input = input("✏️  What would you like to change? ").strip()

                if user_input.lower() in ("exit", "quit", "done", ""):
                    print("👋 Editing session ended.")
                    break

                if user_input.lower() == "preview":
                    print(f"📂 File: {html_file_path}")
                    continue

                if user_input.lower() == "save":
                    with open(html_file_path, "w", encoding="utf-8") as fh:
                        fh.write(self.current_html)
                    print(f"💾 Saved to: {html_file_path}")
                    continue

                print("⏳ Processing …")
                result = self.edit_landing_page(user_input)

                if result["success"]:
                    with open(html_file_path, "w", encoding="utf-8") as fh:
                        fh.write(result["updated_html"])
                    print(f"✅ Edit applied and saved to {html_file_path}")
                else:
                    print(f"❌ Edit failed: {result.get('error')}")

            except KeyboardInterrupt:
                print("\n👋 Session interrupted.")
                return
            except Exception as exc:
                print(f"❌ Unexpected error: {exc}")
                return

        print(f"\n🎉 Editing complete — file at {html_file_path}")

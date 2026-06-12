"""
CLI entry point for the Landing Page Generator.

Usage:
    python -m src.main
"""

import logging

from .business import (
    create_custom_business_info,
    create_sample_business_info,
    get_image_choice,
    get_theme_choice,
)
from .config import load_config
from .system import EnhancedLandingPageCreatorSystem

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Interactive demo / production entry point."""
    print("🚀 ENHANCED LANDING PAGE GENERATOR")
    print("=" * 55)

    try:
        # ── Configuration ────────────────────────────────────
        config = load_config()
        print(f"🤖 LLM provider: {config.llm_provider}")
        if config.llm_provider != "azure":
            print("   Tip: choose image source 'none' or 'pixabay' (DALL-E needs Azure).")
        system = EnhancedLandingPageCreatorSystem(config)

        # ── Business info ────────────────────────────────────
        print("\n" + "=" * 50)
        print("BUSINESS INFORMATION SETUP")
        print("=" * 50)
        print("1. Use sample business (TechFlow Solutions)")
        print("2. Enter custom business information")

        while True:
            try:
                choice = int(input("\nSelect option (1-2): "))
                if choice in (1, 2):
                    break
                print("Please select 1 or 2")
            except ValueError:
                print("Please enter a valid number (1-2)")

        if choice == 1:
            business_info = create_sample_business_info()
            print(f"\n✅ Using sample: {business_info['business_name']}")
        else:
            business_info = create_custom_business_info()
            print(f"\n✅ Custom business: {business_info['business_name']}")

        # ── Theme & image ────────────────────────────────────
        theme = get_theme_choice()
        print(f"✅ Theme: {theme.title()}")

        image_choice, user_image_url = get_image_choice()
        print(f"✅ Image method: {image_choice.title()}")

        # ── Generate ─────────────────────────────────────────
        print("\n🏗️  CREATING LANDING PAGE …")
        print("This may take 2-3 minutes.\n")

        result = system.create_landing_page(
            business_info=business_info,
            image_choice=image_choice,
            user_image_url=user_image_url,
            theme=theme,
        )

        if not result["success"]:
            print(f"\n❌ FAILED: {result.get('error')}")
            return

        # ── Summary ──────────────────────────────────────────
        meta = result["metadata"]
        print("\n" + "=" * 60)
        print("🎉 LANDING PAGE CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"  📄 HTML : {result['files']['html_file']}")
        print(f"  🎨 Theme: {meta['theme'].title()}")
        print(f"  🖼️  Image: {meta['image_source'].title()}")
        print(f"  📦 Sections: {', '.join(result['sections'])}")
        print(f"  ⏱️  Time: {result['generation_time']:.1f}s")
        print(f"  ⏰ Created: {meta['created_at']}")

        # ── Editing ──────────────────────────────────────────
        print("\n" + "=" * 60)
        print("✏️  INTERACTIVE EDITING")
        print("=" * 60)
        print("1. Start interactive editing")
        print("2. Finish and exit")

        while True:
            try:
                edit_choice = int(input("\nSelect option (1-2): "))
                if edit_choice in (1, 2):
                    break
                print("Please select 1 or 2")
            except ValueError:
                print("Please enter a valid number")

        if edit_choice == 1:
            system.editor.start_interactive_editing(result["files"]["html_file"])
        else:
            print(f"\n✅ Done! Open {result['files']['html_file']} in your browser.")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as exc:
        logger.error("Fatal error: %s", exc)
        print(f"\n❌ CRITICAL ERROR: {exc}")


if __name__ == "__main__":
    main()

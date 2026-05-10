"""
Configuration loader and validation.

Reads API credentials from environment variables (loaded via .env)
and exposes them through a validated Config dataclass. This is the
single source of truth for all external service configuration.
"""

import os
import sys
import logging
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    """Immutable application configuration loaded from environment."""

    # Azure OpenAI (GPT)
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment: str
    azure_openai_api_version: str

    # Azure OpenAI (DALL-E 3)  — optional
    dalle_api_key: Optional[str] = None
    dalle_endpoint: Optional[str] = None
    dalle_deployment: Optional[str] = None
    dalle_api_version: str = "2024-02-01"

    # Pixabay — optional
    pixabay_api_key: Optional[str] = None


def load_config(env_path: Optional[str] = None) -> Config:
    """
    Load and validate configuration from environment variables.

    Parameters
    ----------
    env_path : str, optional
        Explicit path to a ``.env`` file.  When *None*, ``python-dotenv``
        searches upward from the current directory.

    Returns
    -------
    Config
        Frozen dataclass containing all validated settings.

    Raises
    ------
    SystemExit
        If any required environment variable is missing or empty.
    """
    load_dotenv(dotenv_path=env_path)

    # ── Required variables ───────────────────────────────────────
    required = {
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION"),
    }

    missing = [k for k, v in required.items() if not v]
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        print(f"\n❌ Missing required environment variables: {', '.join(missing)}")
        print("   Copy .env.example → .env and fill in your credentials.\n")
        sys.exit(1)

    # ── Optional variables (graceful fallback) ───────────────────
    dalle_key = os.getenv("DALLE_API_KEY")
    dalle_endpoint = os.getenv("DALLE_ENDPOINT")
    dalle_deployment = os.getenv("DALLE_DEPLOYMENT_NAME")
    dalle_version = os.getenv("DALLE_API_VERSION", "2024-02-01")
    pixabay_key = os.getenv("PIXABAY_API_KEY")

    config = Config(
        azure_openai_api_key=required["AZURE_OPENAI_API_KEY"],
        azure_openai_endpoint=required["AZURE_OPENAI_ENDPOINT"],
        azure_openai_deployment=required["AZURE_OPENAI_DEPLOYMENT_NAME"],
        azure_openai_api_version=required["AZURE_OPENAI_API_VERSION"],
        dalle_api_key=dalle_key,
        dalle_endpoint=dalle_endpoint,
        dalle_deployment=dalle_deployment,
        dalle_api_version=dalle_version,
        pixabay_api_key=pixabay_key,
    )

    logger.info("Configuration loaded successfully.")
    return config

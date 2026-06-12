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
from typing import Literal, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

LLMProvider = Literal["azure", "groq", "ollama"]


@dataclass(frozen=True)
class Config:
    """Immutable application configuration loaded from environment."""

    llm_provider: LLMProvider

    # Azure OpenAI (GPT) — required when llm_provider=azure
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    azure_openai_api_version: str = "2024-12-01-preview"

    # Groq — free tier at https://console.groq.com
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    groq_base_url: str = "https://api.groq.com/openai/v1"

    # Ollama — local, free at https://ollama.com
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3.2"
    ollama_api_key: str = "ollama"

    # Azure OpenAI (DALL-E 3)  — optional
    dalle_api_key: Optional[str] = None
    dalle_endpoint: Optional[str] = None
    dalle_deployment: Optional[str] = None
    dalle_api_version: str = "2024-02-01"

    # Pixabay — optional (free key at https://pixabay.com/api/docs/)
    pixabay_api_key: Optional[str] = None

    @property
    def llm_uses_max_completion_tokens(self) -> bool:
        return self.llm_provider == "azure"


def _detect_provider() -> LLMProvider:
    explicit = (os.getenv("LLM_PROVIDER") or "").strip().lower()
    if explicit in ("azure", "groq", "ollama"):
        return explicit  # type: ignore[return-value]

    if os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("AZURE_OPENAI_API_KEY"):
        return "azure"
    return "ollama"


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

    provider = _detect_provider()

    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

    groq_key = os.getenv("GROQ_API_KEY")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    groq_base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
    ollama_api_key = os.getenv("OLLAMA_API_KEY", "ollama")

    missing: list[str] = []
    if provider == "azure":
        if not azure_key:
            missing.append("AZURE_OPENAI_API_KEY")
        if not azure_endpoint:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not azure_deployment:
            missing.append("AZURE_OPENAI_DEPLOYMENT_NAME")
    elif provider == "groq":
        if not groq_key:
            missing.append("GROQ_API_KEY")
    # ollama needs no credentials — just a running local server

    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        print(f"\n❌ Missing required environment variables: {', '.join(missing)}")
        print(f"   LLM_PROVIDER is set to '{provider}'.")
        print("   Copy .env.example → .env and fill in your credentials.\n")
        sys.exit(1)

    dalle_key = os.getenv("DALLE_API_KEY")
    dalle_endpoint = os.getenv("DALLE_ENDPOINT")
    dalle_deployment = os.getenv("DALLE_DEPLOYMENT_NAME")
    dalle_version = os.getenv("DALLE_API_VERSION", "2024-02-01")
    pixabay_key = os.getenv("PIXABAY_API_KEY")

    config = Config(
        llm_provider=provider,
        azure_openai_api_key=azure_key,
        azure_openai_endpoint=azure_endpoint,
        azure_openai_deployment=azure_deployment,
        azure_openai_api_version=azure_version,
        groq_api_key=groq_key,
        groq_model=groq_model,
        groq_base_url=groq_base_url,
        ollama_base_url=ollama_base_url,
        ollama_model=ollama_model,
        ollama_api_key=ollama_api_key,
        dalle_api_key=dalle_key,
        dalle_endpoint=dalle_endpoint,
        dalle_deployment=dalle_deployment,
        dalle_api_version=dalle_version,
        pixabay_api_key=pixabay_key,
    )

    logger.info("Configuration loaded successfully (LLM provider: %s).", provider)
    return config

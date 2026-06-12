"""
LLM provider setup — Azure OpenAI, Groq (free tier), or local Ollama.

All providers expose an OpenAI-compatible chat client and an AutoGen
``config_list`` entry so the rest of the pipeline stays unchanged.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Literal, Optional

from openai import AzureOpenAI, OpenAI

from .config import Config

logger = logging.getLogger(__name__)

LLMProvider = Literal["azure", "groq", "ollama"]


@dataclass(frozen=True)
class LLMSetup:
    """Resolved LLM client, model name, and AutoGen configuration."""

    provider: LLMProvider
    client: Any
    model: str
    llm_config: dict
    uses_max_completion_tokens: bool


def create_chat_completion(
    setup: LLMSetup,
    *,
    messages: list,
    max_tokens: int = 100,
    temperature: Optional[float] = None,
) -> str:
    """Run a chat completion and return the assistant message text."""
    kwargs: dict = {
        "model": setup.model,
        "messages": messages,
    }
    if setup.uses_max_completion_tokens:
        kwargs["max_completion_tokens"] = max_tokens
    else:
        kwargs["max_tokens"] = max_tokens
    if temperature is not None:
        kwargs["temperature"] = temperature

    response = setup.client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def build_llm_setup(config: Config) -> LLMSetup:
    """Create the chat client and AutoGen config for the selected provider."""
    if config.llm_provider == "azure":
        client = AzureOpenAI(
            api_key=config.azure_openai_api_key,
            api_version=config.azure_openai_api_version,
            azure_endpoint=config.azure_openai_endpoint,
        )
        llm_config = {
            "config_list": [
                {
                    "model": config.azure_openai_deployment,
                    "api_key": config.azure_openai_api_key,
                    "api_type": "azure",
                    "base_url": config.azure_openai_endpoint,
                    "api_version": config.azure_openai_api_version,
                }
            ],
            "timeout": 300,
        }
        return LLMSetup(
            provider="azure",
            client=client,
            model=config.azure_openai_deployment,
            llm_config=llm_config,
            uses_max_completion_tokens=True,
        )

    if config.llm_provider == "groq":
        base_url = config.groq_base_url or "https://api.groq.com/openai/v1"
        client = OpenAI(api_key=config.groq_api_key, base_url=base_url)
        llm_config = {
            "config_list": [
                {
                    "model": config.groq_model,
                    "api_key": config.groq_api_key,
                    "api_type": "openai",
                    "base_url": base_url,
                }
            ],
            "timeout": 300,
        }
        return LLMSetup(
            provider="groq",
            client=client,
            model=config.groq_model,
            llm_config=llm_config,
            uses_max_completion_tokens=False,
        )

    # ollama — local, no API key required
    base_url = config.ollama_base_url or "http://localhost:11434/v1"
    client = OpenAI(api_key=config.ollama_api_key or "ollama", base_url=base_url)
    llm_config = {
        "config_list": [
            {
                "model": config.ollama_model,
                "api_key": config.ollama_api_key or "ollama",
                "api_type": "openai",
                "base_url": base_url,
            }
        ],
        "timeout": 300,
    }
    return LLMSetup(
        provider="ollama",
        client=client,
        model=config.ollama_model,
        llm_config=llm_config,
        uses_max_completion_tokens=False,
    )


def verify_llm(setup: LLMSetup) -> None:
    """Smoke-test the configured LLM provider."""
    kwargs: dict = {
        "model": setup.model,
        "messages": [{"role": "user", "content": "Hello"}],
    }
    if setup.uses_max_completion_tokens:
        kwargs["max_completion_tokens"] = 10
    else:
        kwargs["max_tokens"] = 10

    setup.client.chat.completions.create(**kwargs)
    label = {
        "azure": f"Azure GPT deployment '{setup.model}'",
        "groq": f"Groq model '{setup.model}'",
        "ollama": f"Ollama model '{setup.model}'",
    }[setup.provider]
    print(f"✅ {label} verified")

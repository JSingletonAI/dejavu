import os
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class LlmConfig(BaseModel):
    provider: str = Field(
        description="Provider of the LLM (e.g., 'venice', 'ollama', 'openai')",
        default=os.environ.get("DEJAVU_LLM_PROVIDER", "venice"),
    )
    config: Optional[dict] = Field(
        description="Configuration for the specific LLM",
        default_factory=lambda: {
            "model": os.environ.get("DEJAVU_LLM_MODEL", "default"),
            "api_key": os.environ.get("VENICE_API_KEY"),
            "base_url": "https://api.venice.ai/api/v1",
            "temperature": 0.0,
        },
    )

    @field_validator("config")
    def validate_config(cls, v, values):
        provider = values.data.get("provider")
        if provider in (
            "venice",
            "openai",
            "ollama",
            "anthropic",
            "groq",
            "together",
            "aws_bedrock",
            "litellm",
            "azure_openai",
            "openai_structured",
            "azure_openai_structured",
            "gemini",
            "deepseek",
            "minimax",
            "xai",
            "sarvam",
            "lmstudio",
            "vllm",
            "langchain",
        ):
            return v
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

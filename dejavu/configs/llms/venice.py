from pydantic import Field

from dejavu.configs.llms.openai import OpenAIConfig


class VeniceConfig(OpenAIConfig):
    provider: str = "venice"
    model: str = Field(default="default")
    api_key: str | None = Field(default=None)
    base_url: str = Field(default="https://api.venice.ai/api/v1")
    temperature: float = Field(default=0.0)
    max_tokens: int | None = Field(default=None)

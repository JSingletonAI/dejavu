import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from dejavu.configs.llms.venice import VeniceConfig
from dejavu.llms.base import LLMBase


def _drop_nulls(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _drop_nulls(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_drop_nulls(v) for v in value]
    return value


class VeniceLLM(LLMBase):
    def __init__(self, config: VeniceConfig | dict | None = None):
        if config is None:
            config = VeniceConfig()
        elif isinstance(config, dict):
            config = VeniceConfig(**config)

        super().__init__(config)

        api_key = self.config.api_key or os.environ.get("VENICE_API_KEY")
        if not api_key:
            raise ValueError("VENICE_API_KEY is required. Run `dejavu init` or export VENICE_API_KEY.")

        self.client = OpenAI(api_key=api_key, base_url=self.config.base_url)

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_format=None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        **kwargs,
    ):
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "response_format": response_format,
            "tools": tools,
            "tool_choice": tool_choice if tools else None,
        }
        payload.update(kwargs)
        response = self.client.chat.completions.create(**_drop_nulls(payload))
        if tools and response.choices[0].message.tool_calls:
            return {
                "content": response.choices[0].message.content,
                "tool_calls": response.choices[0].message.tool_calls,
            }
        return response.choices[0].message.content

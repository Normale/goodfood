"""Claude API client wrapper."""

from typing import Any, Dict, Optional

from anthropic import Anthropic

from src.config.settings import settings


class ClaudeClient:
    """Wrapper for Anthropic Claude API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize Claude client.

        Args:
            api_key: Anthropic API key (defaults to settings)
            model: Model to use (defaults to settings.estimator_model)
        """
        self.client = Anthropic(api_key=api_key or settings.anthropic_api_key)
        self.model = model or settings.estimator_model

    async def query(
        self,
        prompt: str,
        max_tokens: int = 4000,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Send a query to Claude and get response.

        Args:
            prompt: User prompt
            max_tokens: Maximum tokens in response
            system_prompt: Optional system prompt

        Returns:
            Response text from Claude
        """
        messages = [{"role": "user", "content": prompt}]

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        message = self.client.messages.create(**kwargs)
        return message.content[0].text

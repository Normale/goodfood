"""Application settings using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Anthropic API
    anthropic_api_key: str = Field(..., description="Anthropic API key for Claude")

    # MCP Server
    openfoodfacts_mcp_url: str = Field(
        default="http://localhost:3000",
        description="OpenFoodFacts MCP server URL",
    )

    # Workflow Settings
    max_iterations: int = Field(
        default=5,
        description="Maximum iterations for agent negotiation",
    )
    approval_threshold: int = Field(
        default=80,
        description="Minimum approval percentage to reach consensus",
    )
    confidence_threshold: float = Field(
        default=0.7,
        description="Minimum confidence level for estimates",
    )

    # LLM Models
    estimator_model: str = Field(
        default="claude-3-5-haiku-latest",
        description="Model for input agent estimation",
    )
    critic_model: str = Field(
        default="claude-3-5-haiku-latest",
        description="Model for critic agent verification",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )


# Global settings instance
settings = Settings()

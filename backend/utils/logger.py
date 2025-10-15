"""Logging utility for saving LLM prompts and responses."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class LLMLogger:
    """Logger for LLM interactions."""

    def __init__(self, log_dir: str = "logs"):
        """Initialize logger.

        Args:
            log_dir: Directory to save logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

    def log_interaction(
        self,
        agent_name: str,
        prompt: str,
        response: str,
        metadata: Optional[dict] = None,
        ingredient_name: Optional[str] = None,
    ) -> str:
        """Log an LLM interaction to a file.

        Args:
            agent_name: Name of the agent (e.g., 'preprocessing', 'estimator', 'validator')
            prompt: The prompt sent to the LLM
            response: The response from the LLM
            metadata: Optional metadata about the interaction
            ingredient_name: Optional ingredient name for per-ingredient logging

        Returns:
            Path to the log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        # Include ingredient name in filename if provided
        if ingredient_name:
            # Sanitize ingredient name for filename
            safe_name = "".join(c if c.isalnum() else "_" for c in ingredient_name)
            filename = f"{agent_name}_{safe_name}_{timestamp}.txt"
        else:
            filename = f"{agent_name}_{timestamp}.txt"

        filepath = self.log_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"{agent_name.upper()} LOG\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")

            if ingredient_name:
                f.write(f"Ingredient: {ingredient_name}\n")

            if metadata:
                f.write(f"\nMetadata:\n")
                for key, value in metadata.items():
                    f.write(f"  {key}: {value}\n")

            f.write("=" * 80 + "\n\n")

            f.write("PROMPT SENT:\n")
            f.write("=" * 80 + "\n")
            f.write(prompt)
            f.write("\n\n")

            f.write("=" * 80 + "\n")
            f.write("RESPONSE RECEIVED:\n")
            f.write("=" * 80 + "\n")
            f.write(response)
            f.write("\n")

        return str(filepath)


# Global logger instance
_logger = None


def get_logger() -> LLMLogger:
    """Get the global logger instance."""
    global _logger
    if _logger is None:
        _logger = LLMLogger()
    return _logger

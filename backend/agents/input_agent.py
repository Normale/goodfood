"""Input Agent - Estimates nutrients from meal description."""

from integrations.claude_client import ClaudeClient
from config.nutrients import NUTRIENTS


class InputAgent:
    """Estimates nutritional values from meal description."""

    def __init__(self):
        self.client = ClaudeClient()

    async def estimate(self, description: str, feedback: str = None) -> dict:
        """Estimate nutrients from description.

        Args:
            description: Natural language meal description
            feedback: Optional feedback from critic

        Returns:
            Dict with nutrient estimates
        """
        # Build list of nutrients to estimate
        nutrient_names = list(NUTRIENTS.keys())

        prompt = f"""Estimate nutritional values for this meal:

{description}

{f"Previous feedback: {feedback}" if feedback else ""}

Return ONLY a Python dict with these nutrients (use snake_case keys):
{', '.join(nutrient_names)}

Example format:
{{"protein": 25.0, "carbohydrates": 45.0, "vitamin_c": 30.0, ...}}

Provide realistic estimates for ALL nutrients. Use 0.0 if negligible."""

        response = await self.client.query(prompt, max_tokens=2000)

        # Extract dict from response
        try:
            # Find dict in response
            start = response.find("{")
            end = response.rfind("}") + 1
            dict_str = response[start:end]

            # Parse as dict
            estimates = eval(dict_str)  # Simple eval for dict literal
            return estimates

        except Exception as e:
            print(f"Error parsing estimates: {e}")
            # Return zeros as fallback
            return {nutrient: 0.0 for nutrient in nutrient_names}

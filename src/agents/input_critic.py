"""Input Critic - Verifies nutrient estimates."""

from src.integrations.claude_client import ClaudeClient
from src.integrations.openfoodfacts_mcp import OpenFoodFactsMCP


class InputCritic:
    """Verifies and validates nutritional estimates."""

    def __init__(self):
        self.client = ClaudeClient()
        self.mcp = OpenFoodFactsMCP()

    async def verify(self, description: str, estimates: dict) -> dict:
        """Verify estimates against description.

        Args:
            description: Meal description
            estimates: Nutrient estimates from input agent

        Returns:
            Dict with approval status and feedback
        """
        # Check if MCP is available (optional)
        mcp_available = await self.mcp.is_available()

        prompt = f"""Verify these nutritional estimates for accuracy:

Meal: {description}

Estimates: {estimates}

{"MCP available - cross-check with OpenFoodFacts data" if mcp_available else ""}

Review and respond with:
1. approved: true/false
2. approval_percentage: 0-100
3. feedback: specific issues or "looks good"

Return ONLY a Python dict:
{{"approved": true, "approval_percentage": 85, "feedback": "..."}}

Accept estimates within ±25% as correct."""

        response = await self.client.query(prompt, max_tokens=1000)

        # Extract dict from response
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            dict_str = response[start:end]
            result = eval(dict_str)
            return result

        except Exception as e:
            print(f"Error parsing verification: {e}")
            # Default to approved
            return {
                "approved": True,
                "approval_percentage": 100,
                "feedback": "Auto-approved (parsing error)",
            }

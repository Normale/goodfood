"""Nutrition verification agent that challenges and validates estimates."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import anthropic


class NutritionVerifierAgent:
    """Agent that verifies and challenges nutritional estimates for accuracy."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.role = "Nutritional Verifier"
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

    async def verify(self, description: str, estimates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify nutritional estimates and provide detailed feedback.

        Args:
            description: Original meal description
            estimates: Estimates dict from NutritionEstimatorAgent

        Returns:
            Dict with approval status, issues found, feedback, and approval percentage
        """
        prompt = f"""You are a nutritional fact-checker. Your job is to verify estimates and provide feedback.

Meal description: {description}

Estimates to verify:
{json.dumps(estimates.get("estimates", {}), indent=2)}

Your task:
1. Check each nutrient estimate for accuracy based on the meal description
2. Identify specific values that seem significantly off
3. Consider:
   - Typical nutrient profiles of ingredients mentioned
   - Realistic portion sizes for a single meal
   - Bioavailability and cooking losses
   - Nutrient interactions
4. Be specific about what's wrong and what the values should be closer to
5. **IMPORTANT: Accept estimates that are within ±20-25% of expected values as correct**
6. Only flag issues when values are significantly off (more than 25% deviation)
7. Be reasonable and not overly critical - small variations are acceptable

Respond ONLY with valid JSON in this format:
{{
    "approved": true/false,
    "issues_found": [
        {{
            "nutrient": "Vitamin C (mg)",
            "estimated_value": 45,
            "issue": "Too low - based on ingredients, should be closer to 85mg",
            "suggested_value": 85,
            "severity": "high/medium/low"
        }}
    ],
    "overall_feedback": "Summary of main issues (or confirmation if estimates look good)",
    "approval_percentage": <0-100, percentage of estimates that seem correct>
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text

            # Log the conversation
            self._log_message(description, estimates, prompt, response_text)

            # Extract JSON from response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)

            # Format feedback for next iteration
            if result.get("issues_found"):
                feedback_text = f"""
Approval: {result.get("approval_percentage", 0)}%
Overall feedback: {result.get("overall_feedback", "")}

Specific issues to address:
"""
                for issue in result["issues_found"]:
                    feedback_text += f"\n- {issue['nutrient']}: {issue['issue']}"
                    feedback_text += f" (Suggested: {issue.get('suggested_value')})"

                result["feedback"] = feedback_text
            else:
                result["feedback"] = result.get("overall_feedback", "Estimates look good!")

            return result

        except Exception as e:
            error_result = {
                "error": f"Failed to verify nutrition: {str(e)}",
                "approved": False,
                "issues_found": [],
                "overall_feedback": "Error occurred during verification",
                "approval_percentage": 0,
                "feedback": "Verification failed due to error",
            }
            # Log the error
            self._log_message(description, estimates, prompt, f"ERROR: {str(e)}")
            return error_result

    def _log_message(
        self, description: str, estimates: Dict[str, Any], prompt: str, response: str
    ) -> None:
        """Log agent conversation to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file = self.log_dir / f"verifier_{timestamp}.txt"

        with open(log_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"NUTRITION VERIFIER LOG\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"MEAL DESCRIPTION:\n{description}\n\n")

            f.write("ESTIMATES TO VERIFY:\n")
            f.write(json.dumps(estimates.get("estimates", {}), indent=2))
            f.write("\n\n")

            f.write("=" * 80 + "\n")
            f.write("PROMPT SENT:\n")
            f.write("=" * 80 + "\n")
            f.write(f"{prompt}\n\n")

            f.write("=" * 80 + "\n")
            f.write("RESPONSE RECEIVED:\n")
            f.write("=" * 80 + "\n")
            f.write(f"{response}\n")

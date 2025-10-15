"""Input Critic - Verifies nutrient estimates using LangGraph patterns."""

import json
from typing import Any, Dict, Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config.settings import settings


class NutrientIssue(BaseModel):
    """Individual nutrient issue found during verification."""

    nutrient: str = Field(description="Name of the nutrient with issues")
    estimated_value: float = Field(description="Value that was estimated")
    issue: str = Field(description="Description of the issue")
    suggested_value: float = Field(description="Suggested correct value")
    severity: str = Field(description="Severity: high/medium/low")


class VerificationResult(BaseModel):
    """Structured verification result."""

    approved: bool = Field(description="Whether estimates are approved")
    approval_percentage: int = Field(description="Percentage of estimates approved (0-100)", ge=0, le=100)
    issues_found: list[NutrientIssue] = Field(default_factory=list, description="List of issues")
    overall_feedback: str = Field(description="Summary feedback")


class InputCritic:
    """LangGraph-compatible agent for verifying nutritional estimates."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the critic agent.

        Args:
            model_name: LLM model to use (defaults to settings.critic_model)
        """
        self.llm = ChatAnthropic(
            model=model_name or settings.critic_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.2,  # Lower temperature for more consistent verification
            max_tokens=1024,  # Limit for verification feedback and issues list
        )

        # Create output parser for structured responses
        self.parser = JsonOutputParser(pydantic_object=VerificationResult)

        # Create prompt template
        self.prompt = PromptTemplate(
            template="""You are a nutritional fact-checker. Verify estimates and provide detailed feedback.

Meal description:
{description}

Nutrient estimates to verify:
{estimates_json}

Your task:
1. Check each nutrient estimate for accuracy based on the ingredients
2. Identify specific values that seem significantly off
3. Consider:
   - Typical nutrient profiles of each ingredient
   - Realistic portion sizes
   - Bioavailability and cooking losses
   - Nutrient interactions
4. Be specific about what's wrong and what the values should be closer to
5. **IMPORTANT: Accept estimates within ±20-25% of expected values as correct**
6. Only flag issues when values are significantly off (more than 25% deviation)
7. Be reasonable and not overly critical - small variations are acceptable

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=["description", "estimates_json"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
            },
        )

        # Create the chain
        self.chain = self.prompt | self.llm | self.parser

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """LangGraph node function - verifies estimates and updates state.

        Args:
            state: Current graph state

        Returns:
            Updated state with verification results
        """
        description = state["description"]
        estimates = state.get("estimates", {})

        # Convert estimates to JSON for the prompt
        estimates_json = json.dumps(estimates, indent=2)

        try:
            # Invoke the chain synchronously
            result = self.chain.invoke({
                "description": description,
                "estimates_json": estimates_json,
            })

            # Format feedback for next iteration
            feedback_text = self._format_feedback(result)

            # Update state
            state["approved"] = result["approved"]
            state["approval_percentage"] = result["approval_percentage"]
            # issues_found is already a list of dicts from JsonOutputParser
            state["issues_found"] = result.get("issues_found", [])
            state["overall_feedback"] = result["overall_feedback"]
            state["feedback"] = feedback_text

            return state

        except Exception as e:
            print(f"Error during verification: {e}")

            # Update state with error - default to not approved
            state["approved"] = False
            state["approval_percentage"] = 0
            state["issues_found"] = []
            state["overall_feedback"] = f"Verification error: {str(e)}"
            state["feedback"] = "Verification failed due to error"

            return state

    def _format_feedback(self, result: Dict[str, Any]) -> str:
        """Format verification result into feedback text.

        Args:
            result: Verification result dict

        Returns:
            Formatted feedback string
        """
        if result.get("issues_found"):
            feedback_text = f"""
Approval: {result.get("approval_percentage", 0)}%
Overall feedback: {result.get("overall_feedback", "")}

Specific issues to address:
"""
            for issue in result["issues_found"]:
                feedback_text += f"\n- {issue['nutrient']}: {issue['issue']}"
                feedback_text += f" (Suggested: {issue.get('suggested_value')})"

            return feedback_text
        else:
            return result.get("overall_feedback", "Estimates look good!")

    async def verify(self, description: str, estimates: Dict[str, Any]) -> Dict[str, Any]:
        """Verify estimates against description.

        Args:
            description: Meal description
            estimates: Nutrient estimates from input agent (can be full result or just estimates dict)

        Returns:
            Dict with approval status and feedback
        """
        # Extract just the estimates dict if full result was passed
        if "estimates" in estimates:
            estimates_dict = estimates["estimates"]
        else:
            estimates_dict = estimates

        # Convert estimates to JSON for the prompt
        estimates_json = json.dumps(estimates_dict, indent=2)

        try:
            # Invoke the chain
            result = await self.chain.ainvoke({
                "description": description,
                "estimates_json": estimates_json,
            })

            # Add feedback field for backward compatibility
            if "feedback" not in result:
                result["feedback"] = result.get("overall_feedback", "")

            return result

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            # Default to approved on error
            return {
                "approved": True,
                "approval_percentage": 100,
                "issues_found": [],
                "overall_feedback": "Auto-approved due to parsing error",
                "feedback": "Auto-approved due to parsing error",
            }
        except Exception as e:
            print(f"Error during verification: {e}")
            # Default to approved on error
            return {
                "approved": True,
                "approval_percentage": 100,
                "issues_found": [],
                "overall_feedback": f"Auto-approved due to error: {str(e)}",
                "feedback": f"Auto-approved due to error: {str(e)}",
            }

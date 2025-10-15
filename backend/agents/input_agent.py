"""Input Agent - Estimates nutrients from meal description using LangGraph."""

import json
from typing import Any, Dict, Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field, create_model

from config.nutrients import NUTRIENTS, get_formatted_nutrient_list
from config.settings import settings


# Dynamically create Pydantic model for nutrient estimates
def create_nutrient_estimates_model() -> type[BaseModel]:
    """Create Pydantic model with fields for all nutrients."""
    fields = {}
    for nutrient_name in NUTRIENTS.keys():
        # Convert to snake_case for field names
        field_name = nutrient_name.lower().replace(" ", "_").replace("+", "_").replace("-", "_")
        fields[field_name] = (float, Field(default=0.0, description=f"{nutrient_name} value"))

    return create_model("NutrientEstimates", **fields)


NutrientEstimates = create_nutrient_estimates_model()


class EstimationResult(BaseModel):
    """Complete estimation result with metadata."""

    estimates: Dict[str, float] = Field(description="Nutrient estimates")
    reasoning: str = Field(description="Explanation of estimation approach")
    confidence_level: str = Field(description="Confidence: high/medium/low")
    assumptions: list[str] = Field(default_factory=list, description="Key assumptions made")


class InputAgent:
    """LangGraph-compatible agent for nutrient estimation with structured output."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the input agent.

        Args:
            model_name: LLM model to use (defaults to settings.estimator_model)
        """
        self.llm = ChatAnthropic(
            model=model_name or settings.estimator_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.3,
            max_tokens=2048,  # Limit for full meal nutrient estimates + reasoning
        )

        # Create output parser for structured responses
        self.parser = JsonOutputParser(pydantic_object=EstimationResult)

        # Create prompt template
        self.prompt = PromptTemplate(
            template="""You are a nutritional expert. Estimate nutritional values for this meal.

Meal description:
{description}

{feedback_section}

Analyze the meal and provide detailed estimates for ALL these nutrients:
{nutrient_list}

Instructions:
1. Consider typical serving sizes and preparation methods
2. Account for nutrient interactions (e.g., cooking reduces some vitamins)
3. Be specific about quantities - estimate the total amount in the dish
4. For nutrients that are trace/negligible, use 0.0 or very small values
5. If you received feedback, explain what you changed and why

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=["description", "feedback_section"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
                "nutrient_list": get_formatted_nutrient_list(),
            },
        )

        # Create the chain
        self.chain = self.prompt | self.llm | self.parser

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """LangGraph node function - estimates nutrients and updates state.

        Args:
            state: Current graph state

        Returns:
            Updated state with estimation results
        """
        description = state["description"]
        feedback = state.get("feedback")

        feedback_section = (
            f"Previous feedback from verifier:\n{feedback}\n\n"
            "Please revise your estimates based on this feedback."
            if feedback
            else "This is your initial estimation."
        )

        try:
            # Invoke the chain synchronously
            result = self.chain.invoke({
                "description": description,
                "feedback_section": feedback_section,
            })

            # Update state
            state["estimates"] = result["estimates"]
            state["reasoning"] = result["reasoning"]
            state["confidence_level"] = result["confidence_level"]
            state["assumptions"] = result.get("assumptions", [])

            return state

        except Exception as e:
            print(f"Error during estimation: {e}")

            # Update state with error
            state["estimates"] = {nutrient: 0.0 for nutrient in NUTRIENTS.keys()}
            state["reasoning"] = f"Error occurred: {str(e)}"
            state["confidence_level"] = "low"
            state["assumptions"] = ["Error occurred during estimation"]

            return state

    async def estimate(self, description: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """Estimate nutrients from description.

        Args:
            description: Natural language meal description
            feedback: Optional feedback from critic

        Returns:
            Dict with nutrient estimates and metadata
        """
        feedback_section = (
            f"Previous feedback from verifier:\n{feedback}\n\n"
            "Please revise your estimates based on this feedback."
            if feedback
            else "This is your initial estimation."
        )

        try:
            # Invoke the chain
            result = await self.chain.ainvoke({
                "description": description,
                "feedback_section": feedback_section,
            })

            return result

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            # Return default structure
            return {
                "estimates": {nutrient: 0.0 for nutrient in NUTRIENTS.keys()},
                "reasoning": "Failed to parse response",
                "confidence_level": "low",
                "assumptions": ["Error occurred during estimation"],
            }
        except Exception as e:
            print(f"Error during estimation: {e}")
            # Return default structure
            return {
                "estimates": {nutrient: 0.0 for nutrient in NUTRIENTS.keys()},
                "reasoning": f"Error: {str(e)}",
                "confidence_level": "low",
                "assumptions": ["Error occurred during estimation"],
            }

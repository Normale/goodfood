"""Ingredient Estimator - Estimates nutrients for a single ingredient."""

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


class IngredientEstimationResult(BaseModel):
    """Estimation result for a single ingredient."""

    ingredient_name: str = Field(description="Name of the ingredient")
    amount: str = Field(description="Amount with unit")
    estimates: Dict[str, float] = Field(description="Nutrient estimates for this ingredient")
    reasoning: str = Field(description="Brief explanation of estimation")
    confidence_level: str = Field(description="Confidence: high/medium/low")


class IngredientEstimator:
    """Agent that estimates nutrients for a single ingredient."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the ingredient estimator.

        Args:
            model_name: LLM model to use (defaults to settings.estimator_model)
        """
        self.llm = ChatAnthropic(
            model=model_name or settings.estimator_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.3,
        )

        # Create output parser for structured responses
        self.parser = JsonOutputParser(pydantic_object=IngredientEstimationResult)

        # Create prompt template
        self.prompt = PromptTemplate(
            template="""You are a nutritional expert. Estimate nutritional values for a SINGLE ingredient.

Ingredient: {ingredient_name}
Amount: {amount}
Notes: {notes}

Analyze this ingredient and provide estimates for ALL these nutrients:
{nutrient_list}

Instructions:
1. Focus ONLY on this specific ingredient and amount
2. Use standard nutritional databases and knowledge
3. Account for the specific amount given
4. For nutrients that are negligible in this ingredient, use 0.0
5. Be precise - this is for a single ingredient, not a complete meal

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=["ingredient_name", "amount", "notes"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
                "nutrient_list": get_formatted_nutrient_list(),
            },
        )

        # Create the chain
        self.chain = self.prompt | self.llm | self.parser

    async def estimate(
        self,
        ingredient_name: str,
        amount: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Estimate nutrients for a single ingredient.

        Args:
            ingredient_name: Name of the ingredient
            amount: Amount with unit
            notes: Optional notes about the ingredient

        Returns:
            Dict with nutrient estimates
        """
        try:
            # Invoke the chain
            result = await self.chain.ainvoke({
                "ingredient_name": ingredient_name,
                "amount": amount,
                "notes": notes or "None",
            })

            return result

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for {ingredient_name}: {e}")
            # Return default structure
            return {
                "ingredient_name": ingredient_name,
                "amount": amount,
                "estimates": {nutrient: 0.0 for nutrient in NUTRIENTS.keys()},
                "reasoning": "Failed to parse response",
                "confidence_level": "low",
            }
        except Exception as e:
            print(f"Error during estimation for {ingredient_name}: {e}")
            # Return default structure
            return {
                "ingredient_name": ingredient_name,
                "amount": amount,
                "estimates": {nutrient: 0.0 for nutrient in NUTRIENTS.keys()},
                "reasoning": f"Error: {str(e)}",
                "confidence_level": "low",
            }

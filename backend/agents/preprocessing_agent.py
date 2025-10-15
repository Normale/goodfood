"""Preprocessing Agent - Infers ingredients and cooking process from meal description."""

import json
from typing import Any, Dict, Optional, List

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config.settings import settings
from utils.logger import get_logger


class IngredientEstimate(BaseModel):
    """Individual ingredient with estimated quantities."""

    name: str = Field(description="Ingredient name")
    amount: str = Field(description="Estimated amount with unit (e.g., '120g', '1 cup', '2 tablespoons')")
    notes: Optional[str] = Field(default=None, description="Any relevant notes about this ingredient")


class CookingProcess(BaseModel):
    """Information about the cooking process."""

    method: str = Field(description="Primary cooking method (e.g., 'baked', 'fried', 'boiled', 'raw')")
    temperature: Optional[str] = Field(default=None, description="Cooking temperature if applicable")
    duration: Optional[str] = Field(default=None, description="Cooking duration if applicable")
    nutrient_impact: List[str] = Field(
        default_factory=list,
        description="List of likely nutrient impacts (e.g., 'reduces vitamin C', 'increases fat content')"
    )


class PreprocessingResult(BaseModel):
    """Complete preprocessing result."""

    ingredients: List[IngredientEstimate] = Field(description="List of inferred ingredients")
    cooking_process: CookingProcess = Field(description="Inferred cooking process")
    meal_category: str = Field(description="Category (e.g., 'breakfast', 'main dish', 'dessert', 'snack')")
    reasoning: str = Field(description="Explanation of how ingredients were inferred")


class PreprocessingAgent:
    """Agent that preprocesses meal descriptions to infer ingredients and cooking process."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the preprocessing agent.

        Args:
            model_name: LLM model to use (defaults to settings.estimator_model)
        """
        self.llm = ChatAnthropic(
            model=model_name or settings.estimator_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.3,
            max_tokens=1500,  # Limit for ingredient list + cooking process
        )

        # Create output parser for structured responses
        self.parser = JsonOutputParser(pydantic_object=PreprocessingResult)

        # Create prompt template
        self.prompt = PromptTemplate(
            template="""You are a culinary expert specializing in recipe analysis. Given a meal description, infer the likely ingredients, quantities, and cooking process.

Meal description:
{description}

Your task:
1. List ALL likely ingredients with realistic quantities (be specific with amounts and units)
2. Infer the cooking process/method used
3. Identify how the cooking process might affect nutrient content
4. Consider:
   - Standard recipes for this type of dish
   - Typical serving sizes
   - Common ingredient proportions
   - Cooking methods that affect nutrient bioavailability
5. Be comprehensive - include all ingredients even if not explicitly mentioned (oil, salt, etc.)

Examples:
- "pancakes" → 120g all-purpose flour, 2 tablespoons sugar, 1 tablespoon baking powder, 1/2 teaspoon salt, 240ml milk, 1 large egg (65g), 2 tablespoons melted butter
- "grilled chicken salad" → 150g chicken breast, 100g mixed greens, 50g cherry tomatoes, 30g cucumber, 1 tablespoon olive oil, etc.

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=["description"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
            },
        )

        # Create the chain
        self.chain = self.prompt | self.llm | self.parser

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """LangGraph node function - preprocesses meal description and updates state.

        Args:
            state: Current graph state

        Returns:
            Updated state with preprocessing results
        """
        description = state["description"]

        try:
            # Format prompt for logging
            prompt_text = self.prompt.format(description=description)

            # Invoke the chain synchronously
            result = self.chain.invoke({"description": description})

            # Log the interaction
            logger = get_logger()
            logger.log_interaction(
                agent_name="preprocessing",
                prompt=prompt_text,
                response=json.dumps(result, indent=2),
                metadata={"description": description}
            )

            # Update state with preprocessing results
            state["ingredients"] = result["ingredients"]
            state["cooking_process"] = result["cooking_process"]
            state["meal_category"] = result["meal_category"]
            state["preprocessing_reasoning"] = result["reasoning"]

            return state

        except Exception as e:
            print(f"Error during preprocessing: {e}")

            # Update state with error
            state["ingredients"] = []
            state["cooking_process"] = {
                "method": "unknown",
                "nutrient_impact": []
            }
            state["meal_category"] = "unknown"
            state["preprocessing_reasoning"] = f"Error occurred: {str(e)}"

            return state

    async def preprocess(self, description: str) -> Dict[str, Any]:
        """Preprocess meal description.

        Args:
            description: Natural language meal description

        Returns:
            Dict with ingredients and cooking process
        """
        try:
            # Invoke the chain
            result = await self.chain.ainvoke({"description": description})
            return result

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            # Return default structure
            return {
                "ingredients": [],
                "cooking_process": {
                    "method": "unknown",
                    "nutrient_impact": []
                },
                "meal_category": "unknown",
                "reasoning": "Failed to parse response",
            }
        except Exception as e:
            print(f"Error during preprocessing: {e}")
            # Return default structure
            return {
                "ingredients": [],
                "cooking_process": {
                    "method": "unknown",
                    "nutrient_impact": []
                },
                "meal_category": "unknown",
                "reasoning": f"Error: {str(e)}",
            }

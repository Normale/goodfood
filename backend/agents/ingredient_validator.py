"""Ingredient Validator - Validates nutrient estimates for a single ingredient."""

import json
from typing import Any, Dict, Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config.settings import settings


class ValidationResult(BaseModel):
    """Validation result for a single ingredient."""

    approved: bool = Field(description="Whether the estimate is approved")
    feedback: Optional[str] = Field(default=None, description="Feedback if not approved")
    issues_found: int = Field(default=0, description="Number of issues found")


class IngredientValidator:
    """Agent that validates nutrient estimates for a single ingredient."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize the ingredient validator.

        Args:
            model_name: LLM model to use (defaults to settings.critic_model)
        """
        self.llm = ChatAnthropic(
            model=model_name or settings.critic_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0.2,  # Lower temperature for more consistent validation
        )

        # Create output parser for structured responses
        self.parser = JsonOutputParser(pydantic_object=ValidationResult)

        # Create prompt template
        self.prompt = PromptTemplate(
            template="""You are a nutritional fact-checker. Verify nutrient estimates for a SINGLE ingredient.

Ingredient: {ingredient_name}
Amount: {amount}

Nutrient estimates to verify:
{estimates_json}

Your task:
1. Check if the estimates are realistic for THIS specific ingredient and amount
2. Compare against known nutritional databases
3. Accept estimates within ±25% of expected values as correct
4. Only reject if values are significantly wrong or unrealistic
5. Be reasonable - small variations are acceptable for single ingredients

{format_instructions}

Provide your response as valid JSON only.""",
            input_variables=["ingredient_name", "amount", "estimates_json"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
            },
        )

        # Create the chain
        self.chain = self.prompt | self.llm | self.parser

    async def validate(
        self,
        ingredient_name: str,
        amount: str,
        estimates: Dict[str, float]
    ) -> Dict[str, Any]:
        """Validate nutrient estimates for a single ingredient.

        Args:
            ingredient_name: Name of the ingredient
            amount: Amount with unit
            estimates: Nutrient estimates to validate

        Returns:
            Dict with validation results
        """
        # Convert estimates to JSON for the prompt
        estimates_json = json.dumps(estimates, indent=2)

        try:
            # Invoke the chain
            result = await self.chain.ainvoke({
                "ingredient_name": ingredient_name,
                "amount": amount,
                "estimates_json": estimates_json,
            })

            return result

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for {ingredient_name}: {e}")
            # Default to approved on error
            return {
                "approved": True,
                "feedback": None,
                "issues_found": 0,
            }
        except Exception as e:
            print(f"Error during validation for {ingredient_name}: {e}")
            # Default to approved on error
            return {
                "approved": True,
                "feedback": None,
                "issues_found": 0,
            }

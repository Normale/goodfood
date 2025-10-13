"""Nutrition estimation agent with comprehensive nutrient tracking."""

import json
from typing import Any, Dict, List, Optional

import anthropic


COMPREHENSIVE_NUTRIENTS = """
### MACRONUTRIENTS
- Carbohydrates (g)
- Protein (g)
- Total Fats (g)
- Alpha-linolenic acid (g)
- Linoleic acid (g)
- EPA+DHA (mg)
- Soluble Fiber (g)
- Insoluble Fiber (g)
- Water (ml)

### VITAMINS
- Vitamin C (mg)
- Vitamin B1 Thiamine (mg)
- Vitamin B2 Riboflavin (mg)
- Vitamin B3 Niacin (mg)
- Vitamin B5 Pantothenic acid (mg)
- Vitamin B6 Pyridoxine (mg)
- Vitamin B7 Biotin (mcg)
- Vitamin B9 Folate (mcg DFE)
- Vitamin B12 (mcg)
- Vitamin A (mcg RAE)
- Vitamin D (mcg)
- Vitamin E (mg)
- Vitamin K (mcg)

### MINERALS
- Calcium (mg)
- Phosphorus (mg)
- Magnesium (mg)
- Potassium (mg)
- Sodium (mg)
- Chloride (mg)
- Iron (mg)
- Zinc (mg)
- Copper (mcg)
- Selenium (mcg)
- Manganese (mg)
- Iodine (mcg)
- Chromium (mcg)
- Molybdenum (mcg)

### ESSENTIAL AMINO ACIDS
- Leucine (g)
- Lysine (g)
- Valine (g)
- Isoleucine (g)
- Threonine (g)
- Methionine (g)
- Phenylalanine (g)
- Histidine (g)
- Tryptophan (g)

### BENEFICIAL COMPOUNDS
- Choline (mg)
- Taurine (mg)
- CoQ10 (mg)
- Alpha-lipoic acid (mg)
- Beta-glucan (g)
- Resistant starch (g)

### PHYTONUTRIENTS
- Beta-carotene (mg)
- Lycopene (mg)
- Lutein (mg)
- Zeaxanthin (mg)
- Total polyphenols (mg)
- Quercetin (mg)
- Sulforaphane (mg)
- Allicin (mg)
- Curcumin (mg)
"""


class NutritionEstimatorAgent:
    """Agent that estimates comprehensive nutritional values from meal descriptions."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.role = "Nutritional Estimator"

    async def estimate(
        self, description: str, feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Estimate nutritional values for a meal description.

        Args:
            description: Natural language description of the meal
            feedback: Optional feedback from verifier to improve estimates

        Returns:
            Dict containing estimates, reasoning, confidence, and assumptions
        """
        prompt = f"""You are a nutritional expert tasked with estimating the nutritional content of a meal.

Meal description: {description}

{f"Previous feedback from verifier: {feedback}" if feedback else ""}

Analyze this meal and provide a detailed estimate of ALL the following nutrients:
{COMPREHENSIVE_NUTRIENTS}

Instructions:
1. Parse the meal description to identify ingredients and quantities (if provided)
2. If quantities are not specified, assume reasonable portion sizes for a single meal
3. Consider typical serving sizes and preparation methods
4. Account for nutrient interactions (e.g., cooking reduces some vitamins)
5. Be specific about quantities - estimate the total amount in the meal
6. For nutrients that are trace/negligible, still provide a number (can be 0 or very small)
7. If you revised estimates based on feedback, explain what you changed and why

Respond ONLY with valid JSON in this format:
{{
    "estimates": {{
        "Carbohydrates (g)": <number>,
        "Protein (g)": <number>,
        "Total Fats (g)": <number>,
        ... (all {len(COMPREHENSIVE_NUTRIENTS.split('- ')) - 6} nutrients)
    }},
    "reasoning": "Brief explanation of your estimation approach and any changes made",
    "confidence_level": "high/medium/low",
    "assumptions": ["assumption 1", "assumption 2", ...]
}}"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text

            # Extract JSON from response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)

            return result

        except Exception as e:
            return {
                "error": f"Failed to estimate nutrition: {str(e)}",
                "estimates": {},
                "reasoning": "Error occurred during estimation",
                "confidence_level": "low",
                "assumptions": [],
            }

    def extract_macros(self, estimates: Dict[str, float]) -> Dict[str, float]:
        """
        Extract key macronutrients for display.

        Args:
            estimates: Full nutrient estimates dict

        Returns:
            Dict with calories, protein, carbs, fat
        """
        protein = estimates.get("Protein (g)", 0)
        carbs = estimates.get("Carbohydrates (g)", 0)
        fat = estimates.get("Total Fats (g)", 0)

        # Calculate calories (4 cal/g protein, 4 cal/g carbs, 9 cal/g fat)
        calories = (protein * 4) + (carbs * 4) + (fat * 9)

        return {
            "calories": round(calories),
            "protein": round(protein, 1),
            "carbs": round(carbs, 1),
            "fat": round(fat, 1),
        }

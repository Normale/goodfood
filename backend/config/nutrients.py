"""Nutrient definitions - uses canonical keys from nutrition_goals.

IMPORTANT: Import NUTRIENT_KEYS from nutrition_goals as the single source of truth.
"""

from enum import Enum
from typing import Dict, List
from config.nutrition_goals import NUTRIENT_KEYS


class NutrientCategory(str, Enum):
    """Categories of nutrients tracked by the system."""

    MACRONUTRIENT = "macronutrient"
    VITAMIN = "vitamin"
    MINERAL = "mineral"
    AMINO_ACID = "amino_acid"
    BENEFICIAL = "beneficial"
    PHYTONUTRIENT = "phytonutrient"


class NutrientUnit(str, Enum):
    """Standard units for nutrients."""

    GRAM = "g"
    MILLIGRAM = "mg"
    MICROGRAM = "mcg"
    MILLILITER = "ml"


# Complete nutrient list with categories and units
# KEYS ARE CANONICAL - defined in nutrition_goals.NUTRIENT_KEYS
NUTRIENTS: Dict[str, Dict[str, str]] = {
    # Macronutrients
    "carbohydrates": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "protein": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "total-fats": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "alpha-linolenic-acid": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "linoleic-acid": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "epa-dha": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "fiber": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "water": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.MILLILITER},

    # Vitamins
    "vitamin-c": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "thiamine": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "riboflavin": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "niacin": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "pantothenic-acid": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "pyridoxine": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "biotin": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "folate": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "vitamin-b12": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "vitamin-a": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "vitamin-d": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "vitamin-e": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "vitamin-k": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},

    # Minerals
    "calcium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "phosphorus": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "magnesium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "potassium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "sodium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "chloride": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "iron": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "zinc": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "copper": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "selenium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "manganese": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "iodine": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "chromium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "molybdenum": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},

    # Amino Acids
    "leucine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "lysine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "valine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "isoleucine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "threonine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "methionine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "phenylalanine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "histidine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "tryptophan": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},

    # Beneficial Compounds
    "choline": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "taurine": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "coenzyme-q10": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "alpha-lipoic-acid": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "beta-glucan": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.GRAM},
    "resistant-starch": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.GRAM},

    # Phytonutrients
    "beta-carotene": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "lycopene": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "lutein": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "zeaxanthin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "polyphenols": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "quercetin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "sulforaphane": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "allicin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "curcumin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
}


def get_nutrients_by_category(category: NutrientCategory) -> List[str]:
    """Get list of nutrient names by category."""
    return [name for name, info in NUTRIENTS.items() if info["category"] == category]


def get_nutrient_unit(nutrient_name: str) -> str:
    """Get the standard unit for a nutrient."""
    if nutrient_name in NUTRIENTS:
        return NUTRIENTS[nutrient_name]["unit"]
    return "unknown"


def get_formatted_nutrient_list() -> str:
    """Get formatted nutrient list for LLM prompts.

    IMPORTANT: LLM MUST return these EXACT keys in the response.
    """
    output = ["\nIMPORTANT: Use these EXACT nutrient keys in your JSON response:\n"]

    for category in NutrientCategory:
        nutrients = get_nutrients_by_category(category)
        if nutrients:
            output.append(f"\n### {category.value.upper().replace('_', ' ')}")
            for nutrient in nutrients:
                unit = get_nutrient_unit(nutrient)
                output.append(f'- "{nutrient}": value in {unit}')

    return "\n".join(output)

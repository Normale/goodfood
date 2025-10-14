"""Nutrient definitions and categories for the GoodFood system."""

from enum import Enum
from typing import Dict, List

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
NUTRIENTS: Dict[str, Dict[str, str]] = {
    # Macronutrients
    "Carbohydrates": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "Protein": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "Total Fats": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "Alpha-linolenic acid": {
        "category": NutrientCategory.MACRONUTRIENT,
        "unit": NutrientUnit.GRAM,
    },
    "Linoleic acid": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "EPA+DHA": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Soluble Fiber": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "Insoluble Fiber": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.GRAM},
    "Water": {"category": NutrientCategory.MACRONUTRIENT, "unit": NutrientUnit.MILLILITER},
    # Vitamins
    "Vitamin C": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "Vitamin B1 Thiamine": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "Vitamin B2 Riboflavin": {
        "category": NutrientCategory.VITAMIN,
        "unit": NutrientUnit.MILLIGRAM,
    },
    "Vitamin B3 Niacin": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "Vitamin B5 Pantothenic acid": {
        "category": NutrientCategory.VITAMIN,
        "unit": NutrientUnit.MILLIGRAM,
    },
    "Vitamin B6 Pyridoxine": {
        "category": NutrientCategory.VITAMIN,
        "unit": NutrientUnit.MILLIGRAM,
    },
    "Vitamin B7 Biotin": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "Vitamin B9 Folate": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "Vitamin B12": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "Vitamin A": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "Vitamin D": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    "Vitamin E": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MILLIGRAM},
    "Vitamin K": {"category": NutrientCategory.VITAMIN, "unit": NutrientUnit.MICROGRAM},
    # Minerals
    "Calcium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Phosphorus": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Magnesium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Potassium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Sodium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Chloride": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Iron": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Zinc": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Copper": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "Selenium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "Manganese": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MILLIGRAM},
    "Iodine": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "Chromium": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    "Molybdenum": {"category": NutrientCategory.MINERAL, "unit": NutrientUnit.MICROGRAM},
    # Essential Amino Acids
    "Leucine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Lysine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Valine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Isoleucine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Threonine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Methionine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Phenylalanine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Histidine": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    "Tryptophan": {"category": NutrientCategory.AMINO_ACID, "unit": NutrientUnit.GRAM},
    # Beneficial Compounds
    "Choline": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "Taurine": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "CoQ10": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "Alpha-lipoic acid": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.MILLIGRAM},
    "Beta-glucan": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.GRAM},
    "Resistant starch": {"category": NutrientCategory.BENEFICIAL, "unit": NutrientUnit.GRAM},
    # Phytonutrients
    "Beta-carotene": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Lycopene": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Lutein": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Zeaxanthin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Total polyphenols": {
        "category": NutrientCategory.PHYTONUTRIENT,
        "unit": NutrientUnit.MILLIGRAM,
    },
    "Quercetin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Sulforaphane": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Allicin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
    "Curcumin": {"category": NutrientCategory.PHYTONUTRIENT, "unit": NutrientUnit.MILLIGRAM},
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
    """Get formatted nutrient list for LLM prompts."""
    output = []

    for category in NutrientCategory:
        nutrients = get_nutrients_by_category(category)
        if nutrients:
            output.append(f"\n### {category.value.upper().replace('_', ' ')}")
            for nutrient in nutrients:
                unit = get_nutrient_unit(nutrient)
                output.append(f"- {nutrient} ({unit})")

    return "\n".join(output)

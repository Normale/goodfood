"""Nutrition goals and canonical nutrient names.

IMPORTANT: These are the ONLY valid nutrient keys in the system.
All LLMs, models, and code MUST use these exact keys.
"""

from typing import Dict, List

# CANONICAL NUTRIENT NAMES - THE SINGLE SOURCE OF TRUTH
# These exact strings MUST be used everywhere in the system
NUTRIENT_KEYS = [
    # Macronutrients
    "carbohydrates",
    "protein",
    "total-fats",
    "fiber",

    # Essential Fatty Acids
    "alpha-linolenic-acid",
    "linoleic-acid",
    "epa-dha",

    # Water-soluble vitamins
    "vitamin-c",
    "thiamine",
    "riboflavin",
    "niacin",
    "pantothenic-acid",
    "pyridoxine",
    "biotin",
    "folate",
    "vitamin-b12",

    # Fat-soluble vitamins
    "vitamin-a",
    "vitamin-d",
    "vitamin-e",
    "vitamin-k",

    # Major minerals
    "calcium",
    "phosphorus",
    "magnesium",
    "potassium",
    "sodium",
    "chloride",

    # Trace elements
    "iron",
    "zinc",
    "copper",
    "selenium",
    "manganese",
    "iodine",
    "chromium",
    "molybdenum",

    # Amino acids
    "leucine",
    "lysine",
    "valine",
    "isoleucine",
    "threonine",
    "methionine",
    "phenylalanine",
    "histidine",
    "tryptophan",

    # Beneficial compounds
    "choline",
    "taurine",
    "coenzyme-q10",
    "alpha-lipoic-acid",
    "beta-glucan",
    "resistant-starch",

    # Carotenoids
    "beta-carotene",
    "lycopene",
    "lutein",
    "zeaxanthin",

    # Polyphenols
    "polyphenols",
    "quercetin",
    "sulforaphane",
    "allicin",
    "curcumin",

    # Water
    "water",
]

# Daily nutrition goals
NUTRITION_GOALS: Dict[str, Dict[str, any]] = {
    # Macronutrients
    "carbohydrates": {"target": 275, "unit": "g", "min": 225, "max": 325, "priority": "high"},
    "protein": {"target": 87.5, "unit": "g", "min": 84, "max": 91, "priority": "high"},
    "total-fats": {"target": 79.5, "unit": "g", "min": 62, "max": 97, "priority": "high"},
    "fiber": {"target": 38, "unit": "g", "priority": "high"},

    # Essential Fatty Acids
    "alpha-linolenic-acid": {"target": 1.6, "unit": "g", "priority": "high"},
    "linoleic-acid": {"target": 14.5, "unit": "g", "min": 12, "max": 17, "priority": "high"},
    "epa-dha": {"target": 2500, "unit": "mg", "min": 2000, "max": 3000, "priority": "high"},

    # Water-soluble vitamins
    "vitamin-c": {"target": 90, "unit": "mg", "priority": "high"},
    "thiamine": {"target": 1.2, "unit": "mg", "priority": "high"},
    "riboflavin": {"target": 1.3, "unit": "mg", "priority": "high"},
    "niacin": {"target": 16, "unit": "mg", "priority": "high"},
    "pantothenic-acid": {"target": 5, "unit": "mg", "priority": "high"},
    "pyridoxine": {"target": 1.3, "unit": "mg", "priority": "high"},
    "biotin": {"target": 30, "unit": "mcg", "priority": "high"},
    "folate": {"target": 400, "unit": "mcg", "priority": "high"},
    "vitamin-b12": {"target": 2.4, "unit": "mcg", "priority": "high"},

    # Fat-soluble vitamins
    "vitamin-a": {"target": 900, "unit": "mcg", "priority": "high"},
    "vitamin-d": {"target": 17.5, "unit": "mcg", "min": 15, "max": 20, "priority": "high"},
    "vitamin-e": {"target": 15, "unit": "mg", "priority": "high"},
    "vitamin-k": {"target": 120, "unit": "mcg", "priority": "high"},

    # Major minerals
    "calcium": {"target": 1000, "unit": "mg", "priority": "high"},
    "phosphorus": {"target": 700, "unit": "mg", "priority": "high"},
    "magnesium": {"target": 410, "unit": "mg", "min": 400, "max": 420, "priority": "high"},
    "potassium": {"target": 3400, "unit": "mg", "priority": "high"},
    "sodium": {"target": 1500, "unit": "mg", "max": 2300, "priority": "medium"},
    "chloride": {"target": 2300, "unit": "mg", "priority": "medium"},

    # Trace elements
    "iron": {"target": 8, "unit": "mg", "priority": "high"},
    "zinc": {"target": 11, "unit": "mg", "priority": "high"},
    "copper": {"target": 900, "unit": "mcg", "priority": "high"},
    "selenium": {"target": 55, "unit": "mcg", "priority": "high"},
    "manganese": {"target": 2.3, "unit": "mg", "priority": "high"},
    "iodine": {"target": 150, "unit": "mcg", "priority": "high"},
    "chromium": {"target": 35, "unit": "mcg", "priority": "medium"},
    "molybdenum": {"target": 45, "unit": "mcg", "priority": "medium"},

    # Beneficial compounds
    "choline": {"target": 550, "unit": "mg", "priority": "medium"},
    "taurine": {"target": 1750, "unit": "mg", "min": 500, "max": 3000, "priority": "medium"},
    "coenzyme-q10": {"target": 150, "unit": "mg", "min": 100, "max": 200, "priority": "low"},
    "alpha-lipoic-acid": {"target": 450, "unit": "mg", "min": 300, "max": 600, "priority": "low"},

    # Carotenoids and phytonutrients
    "beta-carotene": {"target": 10.5, "unit": "mg", "min": 6, "max": 15, "priority": "medium"},
    "lycopene": {"target": 10.75, "unit": "mg", "min": 6.5, "max": 15, "priority": "medium"},
    "lutein": {"target": 8, "unit": "mg", "min": 6, "max": 10, "priority": "medium"},
    "zeaxanthin": {"target": 3, "unit": "mg", "min": 2, "max": 4, "priority": "medium"},
    "polyphenols": {"target": 825, "unit": "mg", "min": 650, "max": 1000, "priority": "low"},
    "quercetin": {"target": 32.5, "unit": "mg", "min": 15, "max": 50, "priority": "low"},

    # Organosulfur compounds
    "sulforaphane": {"target": 15, "unit": "mg", "min": 10, "max": 20, "priority": "medium"},
    "allicin": {"target": 4.5, "unit": "mg", "min": 3.6, "max": 5.4, "priority": "low"},
    "curcumin": {"target": 750, "unit": "mg", "min": 500, "max": 1000, "priority": "low"},

    # Fiber types
    "beta-glucan": {"target": 6.5, "unit": "g", "min": 3, "max": 10, "priority": "medium"},
    "resistant-starch": {"target": 17.5, "unit": "g", "min": 15, "max": 20, "priority": "medium"},

    # Water
    "water": {"target": 3700, "unit": "ml", "priority": "high"},
}

# Priority mapping for gap analysis
PRIORITY_WEIGHTS = {
    "high": 3,
    "medium": 2,
    "low": 1,
}

def get_nutrient_goal(nutrient_name: str) -> Dict:
    """Get goal information for a specific nutrient.

    Args:
        nutrient_name: Name of the nutrient

    Returns:
        Dict with target, unit, priority, and optional min/max
    """
    return NUTRITION_GOALS.get(nutrient_name, {
        "target": 0,
        "unit": "unknown",
        "priority": "medium"
    })

def get_all_goals() -> Dict[str, Dict]:
    """Get all nutrition goals.

    Returns:
        Dictionary of all nutrition goals
    """
    return NUTRITION_GOALS.copy()

def get_priority_weight(nutrient_name: str) -> int:
    """Get priority weight for a nutrient.

    Args:
        nutrient_name: Name of the nutrient

    Returns:
        Integer weight (3=high, 2=medium, 1=low)
    """
    goal = get_nutrient_goal(nutrient_name)
    priority = goal.get("priority", "medium")
    return PRIORITY_WEIGHTS.get(priority, 2)

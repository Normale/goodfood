"""Nutrition goals for a 25-year-old adult male based on nutrition_guide.md"""

from typing import Dict

# Daily nutrition goals extracted from nutrition_guide.md
# Essential Daily Nutrients (56 total)
NUTRITION_GOALS: Dict[str, Dict[str, any]] = {
    # Macronutrients
    "Carbohydrates": {"target": 275, "unit": "g", "min": 225, "max": 325, "priority": "high"},
    "Protein": {"target": 87.5, "unit": "g", "min": 84, "max": 91, "priority": "high"},
    "Total Fats": {"target": 79.5, "unit": "g", "min": 62, "max": 97, "priority": "high"},
    "Fiber": {"target": 38, "unit": "g", "priority": "high"},

    # Essential Fatty Acids
    "Alpha-Linolenic Acid": {"target": 1.6, "unit": "g", "priority": "high"},
    "Linoleic Acid": {"target": 14.5, "unit": "g", "min": 12, "max": 17, "priority": "high"},
    "EPA+DHA": {"target": 2500, "unit": "mg", "min": 2000, "max": 3000, "priority": "high"},

    # Water-soluble vitamins
    "Vitamin C": {"target": 90, "unit": "mg", "priority": "high"},
    "Thiamine": {"target": 1.2, "unit": "mg", "priority": "high"},
    "Riboflavin": {"target": 1.3, "unit": "mg", "priority": "high"},
    "Niacin": {"target": 16, "unit": "mg", "priority": "high"},
    "Pantothenic Acid": {"target": 5, "unit": "mg", "priority": "high"},
    "Pyridoxine": {"target": 1.3, "unit": "mg", "priority": "high"},
    "Biotin": {"target": 30, "unit": "mcg", "priority": "high"},
    "Folate": {"target": 400, "unit": "mcg", "priority": "high"},
    "Vitamin B12": {"target": 2.4, "unit": "mcg", "priority": "high"},

    # Fat-soluble vitamins
    "Vitamin A": {"target": 900, "unit": "mcg", "priority": "high"},
    "Vitamin D": {"target": 17.5, "unit": "mcg", "min": 15, "max": 20, "priority": "high"},
    "Vitamin E": {"target": 15, "unit": "mg", "priority": "high"},
    "Vitamin K": {"target": 120, "unit": "mcg", "priority": "high"},

    # Major minerals
    "Calcium": {"target": 1000, "unit": "mg", "priority": "high"},
    "Phosphorus": {"target": 700, "unit": "mg", "priority": "high"},
    "Magnesium": {"target": 410, "unit": "mg", "min": 400, "max": 420, "priority": "high"},
    "Potassium": {"target": 3400, "unit": "mg", "priority": "high"},
    "Sodium": {"target": 1500, "unit": "mg", "max": 2300, "priority": "medium"},
    "Chloride": {"target": 2300, "unit": "mg", "priority": "medium"},

    # Trace elements
    "Iron": {"target": 8, "unit": "mg", "priority": "high"},
    "Zinc": {"target": 11, "unit": "mg", "priority": "high"},
    "Copper": {"target": 900, "unit": "mcg", "priority": "high"},
    "Selenium": {"target": 55, "unit": "mcg", "priority": "high"},
    "Manganese": {"target": 2.3, "unit": "mg", "priority": "high"},
    "Iodine": {"target": 150, "unit": "mcg", "priority": "high"},
    "Chromium": {"target": 35, "unit": "mcg", "priority": "medium"},
    "Molybdenum": {"target": 45, "unit": "mcg", "priority": "medium"},

    # Beneficial compounds (Priority 2-3)
    "Choline": {"target": 550, "unit": "mg", "priority": "medium"},
    "Taurine": {"target": 1750, "unit": "mg", "min": 500, "max": 3000, "priority": "medium"},
    "Coenzyme Q10": {"target": 150, "unit": "mg", "min": 100, "max": 200, "priority": "low"},
    "Alpha-Lipoic Acid": {"target": 450, "unit": "mg", "min": 300, "max": 600, "priority": "low"},

    # Carotenoids and phytonutrients
    "Beta-Carotene": {"target": 10.5, "unit": "mg", "min": 6, "max": 15, "priority": "medium"},
    "Lycopene": {"target": 10.75, "unit": "mg", "min": 6.5, "max": 15, "priority": "medium"},
    "Lutein": {"target": 8, "unit": "mg", "min": 6, "max": 10, "priority": "medium"},
    "Zeaxanthin": {"target": 3, "unit": "mg", "min": 2, "max": 4, "priority": "medium"},
    "Polyphenols": {"target": 825, "unit": "mg", "min": 650, "max": 1000, "priority": "low"},
    "Quercetin": {"target": 32.5, "unit": "mg", "min": 15, "max": 50, "priority": "low"},

    # Organosulfur compounds
    "Sulforaphane": {"target": 15, "unit": "mg", "min": 10, "max": 20, "priority": "medium"},
    "Allicin": {"target": 4.5, "unit": "mg", "min": 3.6, "max": 5.4, "priority": "low"},
    "Curcumin": {"target": 750, "unit": "mg", "min": 500, "max": 1000, "priority": "low"},

    # Fiber types
    "Beta-Glucan": {"target": 6.5, "unit": "g", "min": 3, "max": 10, "priority": "medium"},
    "Resistant Starch": {"target": 17.5, "unit": "g", "min": 15, "max": 20, "priority": "medium"},

    # Water
    "Water": {"target": 3700, "unit": "ml", "priority": "high"},
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

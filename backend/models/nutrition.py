"""Simplified nutrition data models."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MealType(str, Enum):
    """Types of meals."""

    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class NutritionRecord(BaseModel):
    """Nutrition record."""

    id: UUID
    timestamp: datetime
    name: str
    description: str
    meal_type: MealType

    # All nutrients as individual fields
    carbohydrates: float = 0.0
    protein: float = 0.0
    total_fats: float = 0.0
    alpha_linolenic_acid: float = 0.0
    linoleic_acid: float = 0.0
    epa_dha: float = 0.0
    soluble_fiber: float = 0.0
    insoluble_fiber: float = 0.0
    water: float = 0.0

    vitamin_c: float = 0.0
    vitamin_b1_thiamine: float = 0.0
    vitamin_b2_riboflavin: float = 0.0
    vitamin_b3_niacin: float = 0.0
    vitamin_b5_pantothenic_acid: float = 0.0
    vitamin_b6_pyridoxine: float = 0.0
    vitamin_b7_biotin: float = 0.0
    vitamin_b9_folate: float = 0.0
    vitamin_b12: float = 0.0
    vitamin_a: float = 0.0
    vitamin_d: float = 0.0
    vitamin_e: float = 0.0
    vitamin_k: float = 0.0

    calcium: float = 0.0
    phosphorus: float = 0.0
    magnesium: float = 0.0
    potassium: float = 0.0
    sodium: float = 0.0
    chloride: float = 0.0
    iron: float = 0.0
    zinc: float = 0.0
    copper: float = 0.0
    selenium: float = 0.0
    manganese: float = 0.0
    iodine: float = 0.0
    chromium: float = 0.0
    molybdenum: float = 0.0

    leucine: float = 0.0
    lysine: float = 0.0
    valine: float = 0.0
    isoleucine: float = 0.0
    threonine: float = 0.0
    methionine: float = 0.0
    phenylalanine: float = 0.0
    histidine: float = 0.0
    tryptophan: float = 0.0

    choline: float = 0.0
    taurine: float = 0.0
    coq10: float = 0.0
    alpha_lipoic_acid: float = 0.0
    beta_glucan: float = 0.0
    resistant_starch: float = 0.0

    beta_carotene: float = 0.0
    lycopene: float = 0.0
    lutein: float = 0.0
    zeaxanthin: float = 0.0
    total_polyphenols: float = 0.0
    quercetin: float = 0.0
    sulforaphane: float = 0.0
    allicin: float = 0.0
    curcumin: float = 0.0

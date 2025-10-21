"""Tortoise ORM database models."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """User model."""

    id = fields.UUIDField(primary_key=True, default=uuid4)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"


class Ingredient(Model):
    """Ingredient model - cache for commonly used ingredients."""

    id = fields.UUIDField(primary_key=True, default=uuid4)
    name = fields.TextField()
    description = fields.TextField(null=True)
    reasoning = fields.TextField(null=True)  # AI reasoning about this ingredient

    # Macronutrients
    calories = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    carbohydrates = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    protein = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_fats = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    alpha_linolenic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    linoleic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    epa_dha = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    soluble_fiber = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    insoluble_fiber = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    water = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Vitamins
    vitamin_c = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b1_thiamine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b2_riboflavin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b3_niacin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b5_pantothenic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b6_pyridoxine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b7_biotin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b9_folate = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b12 = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_a = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_d = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_e = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_k = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Minerals
    calcium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    phosphorus = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    magnesium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    potassium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    sodium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    chloride = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    iron = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    zinc = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    copper = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    selenium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    manganese = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    iodine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    chromium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    molybdenum = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Amino Acids
    leucine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    lysine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    valine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    isoleucine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    threonine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    methionine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    phenylalanine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    histidine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    tryptophan = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Beneficial Compounds
    choline = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    taurine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    coq10 = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    alpha_lipoic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    beta_glucan = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    resistant_starch = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Phytonutrients
    beta_carotene = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    lycopene = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    lutein = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    zeaxanthin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_polyphenols = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    quercetin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    sulforaphane = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    allicin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    curcumin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "ingredients"


class UserFood(Model):
    """User's food - can be user-created, from external DB, or copied from ingredients."""

    id = fields.UUIDField(primary_key=True, default=uuid4)
    user = fields.ForeignKeyField("models.User", related_name="foods", on_delete=fields.CASCADE)
    source = fields.TextField(null=True)  # e.g., "openfoodfacts", "usda", "manual"
    source_key = fields.TextField(null=True)  # Reference key in the source system

    name = fields.TextField()
    description = fields.TextField(null=True)

    # Macronutrients
    calories = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    carbohydrates = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    protein = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_fats = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    alpha_linolenic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    linoleic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    epa_dha = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    soluble_fiber = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    insoluble_fiber = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    water = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Vitamins
    vitamin_c = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b1_thiamine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b2_riboflavin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b3_niacin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b5_pantothenic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b6_pyridoxine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b7_biotin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b9_folate = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_b12 = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_a = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_d = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_e = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    vitamin_k = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Minerals
    calcium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    phosphorus = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    magnesium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    potassium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    sodium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    chloride = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    iron = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    zinc = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    copper = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    selenium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    manganese = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    iodine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    chromium = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    molybdenum = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Amino Acids
    leucine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    lysine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    valine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    isoleucine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    threonine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    methionine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    phenylalanine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    histidine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    tryptophan = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Beneficial Compounds
    choline = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    taurine = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    coq10 = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    alpha_lipoic_acid = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    beta_glucan = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    resistant_starch = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Phytonutrients
    beta_carotene = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    lycopene = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    lutein = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    zeaxanthin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_polyphenols = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    quercetin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    sulforaphane = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    allicin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    curcumin = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    # AI vectors (pgvector extension) - will be populated by triggers
    # Note: Tortoise ORM doesn't have native pgvector support, these will be managed via raw SQL
    # vector_nutrition: 60-dimensional normalized nutrition vector
    # vector_description: 384-dimensional description embedding

    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_foods"


class FoodLog(Model):
    """Food log entry - tracks when user ate what food."""

    id = fields.UUIDField(primary_key=True, default=uuid4)
    user = fields.ForeignKeyField("models.User", related_name="food_logs", on_delete=fields.CASCADE)
    user_food = fields.ForeignKeyField("models.UserFood", related_name="logs")
    eaten_at = fields.DatetimeField(auto_now_add=True)
    amount_grams = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    meal_type = fields.CharField(max_length=50, null=True)  # breakfast, lunch, dinner, snack
    extra = fields.JSONField(null=True)  # Extra metadata about the log entry

    class Meta:
        table = "food_logs"

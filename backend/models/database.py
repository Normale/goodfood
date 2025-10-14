"""Database models with all nutrients as columns."""

from datetime import datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NutritionHistory(Base):
    """Nutrition history with all nutrients as columns."""

    __tablename__ = "nutrition_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    meal_type = Column(String(50), index=True)

    # Embeddings
    description_embedding = Column(Vector(1536))  # From description text
    nutrient_profile_embedding = Column(Vector(1536))  # Normalized nutrient vector

    # Macronutrients
    carbohydrates = Column(Float, default=0.0)
    protein = Column(Float, default=0.0)
    total_fats = Column(Float, default=0.0)
    alpha_linolenic_acid = Column(Float, default=0.0)
    linoleic_acid = Column(Float, default=0.0)
    epa_dha = Column(Float, default=0.0)
    soluble_fiber = Column(Float, default=0.0)
    insoluble_fiber = Column(Float, default=0.0)
    water = Column(Float, default=0.0)

    # Vitamins
    vitamin_c = Column(Float, default=0.0)
    vitamin_b1_thiamine = Column(Float, default=0.0)
    vitamin_b2_riboflavin = Column(Float, default=0.0)
    vitamin_b3_niacin = Column(Float, default=0.0)
    vitamin_b5_pantothenic_acid = Column(Float, default=0.0)
    vitamin_b6_pyridoxine = Column(Float, default=0.0)
    vitamin_b7_biotin = Column(Float, default=0.0)
    vitamin_b9_folate = Column(Float, default=0.0)
    vitamin_b12 = Column(Float, default=0.0)
    vitamin_a = Column(Float, default=0.0)
    vitamin_d = Column(Float, default=0.0)
    vitamin_e = Column(Float, default=0.0)
    vitamin_k = Column(Float, default=0.0)

    # Minerals
    calcium = Column(Float, default=0.0)
    phosphorus = Column(Float, default=0.0)
    magnesium = Column(Float, default=0.0)
    potassium = Column(Float, default=0.0)
    sodium = Column(Float, default=0.0)
    chloride = Column(Float, default=0.0)
    iron = Column(Float, default=0.0)
    zinc = Column(Float, default=0.0)
    copper = Column(Float, default=0.0)
    selenium = Column(Float, default=0.0)
    manganese = Column(Float, default=0.0)
    iodine = Column(Float, default=0.0)
    chromium = Column(Float, default=0.0)
    molybdenum = Column(Float, default=0.0)

    # Essential Amino Acids
    leucine = Column(Float, default=0.0)
    lysine = Column(Float, default=0.0)
    valine = Column(Float, default=0.0)
    isoleucine = Column(Float, default=0.0)
    threonine = Column(Float, default=0.0)
    methionine = Column(Float, default=0.0)
    phenylalanine = Column(Float, default=0.0)
    histidine = Column(Float, default=0.0)
    tryptophan = Column(Float, default=0.0)

    # Beneficial Compounds
    choline = Column(Float, default=0.0)
    taurine = Column(Float, default=0.0)
    coq10 = Column(Float, default=0.0)
    alpha_lipoic_acid = Column(Float, default=0.0)
    beta_glucan = Column(Float, default=0.0)
    resistant_starch = Column(Float, default=0.0)

    # Phytonutrients
    beta_carotene = Column(Float, default=0.0)
    lycopene = Column(Float, default=0.0)
    lutein = Column(Float, default=0.0)
    zeaxanthin = Column(Float, default=0.0)
    total_polyphenols = Column(Float, default=0.0)
    quercetin = Column(Float, default=0.0)
    sulforaphane = Column(Float, default=0.0)
    allicin = Column(Float, default=0.0)
    curcumin = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

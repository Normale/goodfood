"""Initial schema with nutrition_history table and all nutrient columns.

Revision ID: 001
Revises:
Create Date: 2025-10-06

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create nutrition_history table with all nutrient columns."""
    # Create pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create nutrition_history table
    op.create_table(
        "nutrition_history",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(1000)),
        sa.Column("meal_type", sa.String(50)),
        # Embeddings
        sa.Column("description_embedding", Vector(1536)),
        sa.Column("nutrient_profile_embedding", Vector(1536)),
        # Macronutrients
        sa.Column("carbohydrates", sa.Float, default=0.0),
        sa.Column("protein", sa.Float, default=0.0),
        sa.Column("total_fats", sa.Float, default=0.0),
        sa.Column("alpha_linolenic_acid", sa.Float, default=0.0),
        sa.Column("linoleic_acid", sa.Float, default=0.0),
        sa.Column("epa_dha", sa.Float, default=0.0),
        sa.Column("soluble_fiber", sa.Float, default=0.0),
        sa.Column("insoluble_fiber", sa.Float, default=0.0),
        sa.Column("water", sa.Float, default=0.0),
        # Vitamins
        sa.Column("vitamin_c", sa.Float, default=0.0),
        sa.Column("vitamin_b1_thiamine", sa.Float, default=0.0),
        sa.Column("vitamin_b2_riboflavin", sa.Float, default=0.0),
        sa.Column("vitamin_b3_niacin", sa.Float, default=0.0),
        sa.Column("vitamin_b5_pantothenic_acid", sa.Float, default=0.0),
        sa.Column("vitamin_b6_pyridoxine", sa.Float, default=0.0),
        sa.Column("vitamin_b7_biotin", sa.Float, default=0.0),
        sa.Column("vitamin_b9_folate", sa.Float, default=0.0),
        sa.Column("vitamin_b12", sa.Float, default=0.0),
        sa.Column("vitamin_a", sa.Float, default=0.0),
        sa.Column("vitamin_d", sa.Float, default=0.0),
        sa.Column("vitamin_e", sa.Float, default=0.0),
        sa.Column("vitamin_k", sa.Float, default=0.0),
        # Minerals
        sa.Column("calcium", sa.Float, default=0.0),
        sa.Column("phosphorus", sa.Float, default=0.0),
        sa.Column("magnesium", sa.Float, default=0.0),
        sa.Column("potassium", sa.Float, default=0.0),
        sa.Column("sodium", sa.Float, default=0.0),
        sa.Column("chloride", sa.Float, default=0.0),
        sa.Column("iron", sa.Float, default=0.0),
        sa.Column("zinc", sa.Float, default=0.0),
        sa.Column("copper", sa.Float, default=0.0),
        sa.Column("selenium", sa.Float, default=0.0),
        sa.Column("manganese", sa.Float, default=0.0),
        sa.Column("iodine", sa.Float, default=0.0),
        sa.Column("chromium", sa.Float, default=0.0),
        sa.Column("molybdenum", sa.Float, default=0.0),
        # Amino Acids
        sa.Column("leucine", sa.Float, default=0.0),
        sa.Column("lysine", sa.Float, default=0.0),
        sa.Column("valine", sa.Float, default=0.0),
        sa.Column("isoleucine", sa.Float, default=0.0),
        sa.Column("threonine", sa.Float, default=0.0),
        sa.Column("methionine", sa.Float, default=0.0),
        sa.Column("phenylalanine", sa.Float, default=0.0),
        sa.Column("histidine", sa.Float, default=0.0),
        sa.Column("tryptophan", sa.Float, default=0.0),
        # Beneficial Compounds
        sa.Column("choline", sa.Float, default=0.0),
        sa.Column("taurine", sa.Float, default=0.0),
        sa.Column("coq10", sa.Float, default=0.0),
        sa.Column("alpha_lipoic_acid", sa.Float, default=0.0),
        sa.Column("beta_glucan", sa.Float, default=0.0),
        sa.Column("resistant_starch", sa.Float, default=0.0),
        # Phytonutrients
        sa.Column("beta_carotene", sa.Float, default=0.0),
        sa.Column("lycopene", sa.Float, default=0.0),
        sa.Column("lutein", sa.Float, default=0.0),
        sa.Column("zeaxanthin", sa.Float, default=0.0),
        sa.Column("total_polyphenols", sa.Float, default=0.0),
        sa.Column("quercetin", sa.Float, default=0.0),
        sa.Column("sulforaphane", sa.Float, default=0.0),
        sa.Column("allicin", sa.Float, default=0.0),
        sa.Column("curcumin", sa.Float, default=0.0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Create indices
    op.create_index("idx_timestamp", "nutrition_history", ["timestamp"])
    op.create_index("idx_meal_type", "nutrition_history", ["meal_type"])
    op.create_index("idx_name", "nutrition_history", ["name"])

    # Create vector indices
    op.execute(
        """
        CREATE INDEX idx_description_embedding ON nutrition_history
        USING ivfflat (description_embedding vector_cosine_ops)
        WITH (lists = 100)
        """
    )

    op.execute(
        """
        CREATE INDEX idx_nutrient_profile ON nutrition_history
        USING ivfflat (nutrient_profile_embedding vector_cosine_ops)
        WITH (lists = 100)
        """
    )


def downgrade() -> None:
    """Drop nutrition_history table."""
    op.drop_table("nutrition_history")
    op.execute("DROP EXTENSION IF EXISTS vector")

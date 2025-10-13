"""Simplified database gateway."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_db_session
from src.models.database import NutritionHistory
from src.models.nutrition import MealType, NutritionRecord


class DatabaseGateway:
    """Gateway for database operations."""

    async def save_nutrition(
        self,
        name: str,
        description: str,
        meal_type: MealType,
        nutrients: dict,
        timestamp: Optional[datetime] = None,
        description_embedding: Optional[List[float]] = None,
        nutrient_profile_embedding: Optional[List[float]] = None,
    ) -> NutritionRecord:
        """Save nutrition record.

        Args:
            name: Meal name
            description: Meal description
            meal_type: Type of meal
            nutrients: Dictionary of nutrient values
            timestamp: When meal was consumed (defaults to now)
            description_embedding: Text embedding from description
            nutrient_profile_embedding: Normalized nutrient vector

        Returns:
            Saved NutritionRecord
        """
        timestamp = timestamp or datetime.now()

        async with get_db_session() as session:
            record = NutritionHistory(
                timestamp=timestamp,
                name=name,
                description=description,
                meal_type=meal_type.value,
                description_embedding=description_embedding,
                nutrient_profile_embedding=nutrient_profile_embedding,
                **nutrients,  # All nutrient fields
            )

            session.add(record)
            await session.flush()

            # Convert to Pydantic model
            return self._to_pydantic(record)

    async def get_history(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        meal_type: Optional[MealType] = None,
        limit: int = 100,
    ) -> List[NutritionRecord]:
        """Get nutrition history.

        Args:
            start_date: Start date filter
            end_date: End date filter
            meal_type: Meal type filter
            limit: Maximum number of records

        Returns:
            List of NutritionRecord objects
        """
        async with get_db_session() as session:
            query = select(NutritionHistory).order_by(NutritionHistory.timestamp.desc())

            if start_date:
                query = query.where(NutritionHistory.timestamp >= start_date)
            if end_date:
                query = query.where(NutritionHistory.timestamp <= end_date)
            if meal_type:
                query = query.where(NutritionHistory.meal_type == meal_type.value)

            query = query.limit(limit)

            result = await session.execute(query)
            records = result.scalars().all()

            return [self._to_pydantic(r) for r in records]

    async def get_by_id(self, record_id: UUID) -> Optional[NutritionRecord]:
        """Get nutrition record by ID."""
        async with get_db_session() as session:
            result = await session.execute(
                select(NutritionHistory).where(NutritionHistory.id == record_id)
            )
            record = result.scalar_one_or_none()

            if not record:
                return None

            return self._to_pydantic(record)

    async def search_similar_by_description(
        self,
        embedding: List[float],
        limit: int = 10,
    ) -> List[NutritionRecord]:
        """Search for similar meals by description embedding.

        Args:
            embedding: Description embedding vector
            limit: Number of results

        Returns:
            List of similar meals
        """
        async with get_db_session() as session:
            # TODO: Implement vector similarity search
            # Example: SELECT * FROM nutrition_history
            # ORDER BY description_embedding <=> '[...]' LIMIT 10
            pass

    async def search_similar_by_nutrients(
        self,
        embedding: List[float],
        limit: int = 10,
    ) -> List[NutritionRecord]:
        """Search for similar meals by nutrient profile.

        Args:
            embedding: Nutrient profile embedding vector
            limit: Number of results

        Returns:
            List of nutritionally similar meals
        """
        async with get_db_session() as session:
            # TODO: Implement vector similarity search
            pass

    def _to_pydantic(self, record: NutritionHistory) -> NutritionRecord:
        """Convert SQLAlchemy model to Pydantic."""
        return NutritionRecord(
            id=record.id,
            timestamp=record.timestamp,
            name=record.name,
            description=record.description or "",
            meal_type=MealType(record.meal_type),
            carbohydrates=record.carbohydrates,
            protein=record.protein,
            total_fats=record.total_fats,
            alpha_linolenic_acid=record.alpha_linolenic_acid,
            linoleic_acid=record.linoleic_acid,
            epa_dha=record.epa_dha,
            soluble_fiber=record.soluble_fiber,
            insoluble_fiber=record.insoluble_fiber,
            water=record.water,
            vitamin_c=record.vitamin_c,
            vitamin_b1_thiamine=record.vitamin_b1_thiamine,
            vitamin_b2_riboflavin=record.vitamin_b2_riboflavin,
            vitamin_b3_niacin=record.vitamin_b3_niacin,
            vitamin_b5_pantothenic_acid=record.vitamin_b5_pantothenic_acid,
            vitamin_b6_pyridoxine=record.vitamin_b6_pyridoxine,
            vitamin_b7_biotin=record.vitamin_b7_biotin,
            vitamin_b9_folate=record.vitamin_b9_folate,
            vitamin_b12=record.vitamin_b12,
            vitamin_a=record.vitamin_a,
            vitamin_d=record.vitamin_d,
            vitamin_e=record.vitamin_e,
            vitamin_k=record.vitamin_k,
            calcium=record.calcium,
            phosphorus=record.phosphorus,
            magnesium=record.magnesium,
            potassium=record.potassium,
            sodium=record.sodium,
            chloride=record.chloride,
            iron=record.iron,
            zinc=record.zinc,
            copper=record.copper,
            selenium=record.selenium,
            manganese=record.manganese,
            iodine=record.iodine,
            chromium=record.chromium,
            molybdenum=record.molybdenum,
            leucine=record.leucine,
            lysine=record.lysine,
            valine=record.valine,
            isoleucine=record.isoleucine,
            threonine=record.threonine,
            methionine=record.methionine,
            phenylalanine=record.phenylalanine,
            histidine=record.histidine,
            tryptophan=record.tryptophan,
            choline=record.choline,
            taurine=record.taurine,
            coq10=record.coq10,
            alpha_lipoic_acid=record.alpha_lipoic_acid,
            beta_glucan=record.beta_glucan,
            resistant_starch=record.resistant_starch,
            beta_carotene=record.beta_carotene,
            lycopene=record.lycopene,
            lutein=record.lutein,
            zeaxanthin=record.zeaxanthin,
            total_polyphenols=record.total_polyphenols,
            quercetin=record.quercetin,
            sulforaphane=record.sulforaphane,
            allicin=record.allicin,
            curcumin=record.curcumin,
        )

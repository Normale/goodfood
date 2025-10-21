"""Database integration using Tortoise ORM."""

import logging
from pathlib import Path
from typing import Optional
from uuid import UUID

from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from config.settings import settings
from models.database import FoodLog, Ingredient, User, UserFood

logger = logging.getLogger(__name__)

# Default user ID (created in migration)
DEFAULT_USER_ID = UUID("00000000-0000-0000-0000-000000000000")


async def init_database() -> None:
    """Initialize database connection and run migrations."""
    logger.info("Initializing database connection...")

    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models.database"]},
    )

    # Run migrations
    await run_migrations()

    logger.info("Database initialized successfully")


async def run_migrations() -> None:
    """Run SQL migrations."""
    logger.info("Running database migrations...")

    # Get database connection
    conn = Tortoise.get_connection("default")

    # Check if tables exist
    tables_exist = await conn.execute_query(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'users'
        );
        """
    )

    if not tables_exist[0][0]:
        logger.info("Tables do not exist, running initial migration...")

        # Read and execute migration file
        migration_file = Path(__file__).parent.parent / "migrations" / "001_initial_schema.sql"
        if migration_file.exists():
            migration_sql = migration_file.read_text()
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in migration_sql.split(";") if s.strip()]
            for statement in statements:
                try:
                    await conn.execute_script(statement)
                except Exception as e:
                    logger.warning(f"Migration statement warning: {e}")
                    # Continue with other statements

            logger.info("Initial migration completed")
        else:
            logger.error(f"Migration file not found: {migration_file}")
    else:
        logger.info("Tables already exist, skipping migration")


async def close_database() -> None:
    """Close database connections."""
    logger.info("Closing database connections...")
    await Tortoise.close_connections()
    logger.info("Database connections closed")


async def get_default_user() -> User:
    """Get or create the default user."""
    try:
        user = await User.get(id=DEFAULT_USER_ID)
    except DoesNotExist:
        # Create default user if it doesn't exist
        user = await User.create(
            id=DEFAULT_USER_ID,
            username="default_user",
            email="default@goodfood.local",
        )
        logger.info("Created default user")

    return user


async def create_user_food(
    name: str,
    description: Optional[str] = None,
    nutrients: Optional[dict] = None,
    source: Optional[str] = None,
    source_key: Optional[str] = None,
    user_id: UUID = DEFAULT_USER_ID,
) -> UserFood:
    """Create a user food entry with nutritional data.

    Args:
        name: Food name
        description: Food description
        nutrients: Dictionary of nutrient values
        source: Source of the food data (e.g., "openfoodfacts")
        source_key: Key/ID in the source system
        user_id: User ID (defaults to default user)

    Returns:
        Created UserFood instance
    """
    food_data = {
        "user_id": user_id,
        "name": name,
        "description": description,
        "source": source,
        "source_key": source_key,
    }

    # Add nutrients if provided
    if nutrients:
        food_data.update(nutrients)

    food = await UserFood.create(**food_data)
    logger.debug(f"Created user food: {name} (ID: {food.id})")

    return food


async def log_food(
    user_food_id: UUID,
    amount_grams: Optional[float] = None,
    meal_type: Optional[str] = None,
    extra: Optional[dict] = None,
    user_id: UUID = DEFAULT_USER_ID,
) -> FoodLog:
    """Log a food consumption entry.

    Args:
        user_food_id: ID of the user food
        amount_grams: Amount consumed in grams
        meal_type: Type of meal (breakfast, lunch, dinner, snack)
        extra: Extra metadata
        user_id: User ID (defaults to default user)

    Returns:
        Created FoodLog instance
    """
    log = await FoodLog.create(
        user_id=user_id,
        user_food_id=user_food_id,
        amount_grams=amount_grams,
        meal_type=meal_type,
        extra=extra,
    )
    logger.debug(f"Created food log: {log.id}")

    return log


async def get_food_logs_by_date_range(
    start_date,
    end_date,
    user_id: UUID = DEFAULT_USER_ID,
) -> list[FoodLog]:
    """Get food logs within a date range.

    Args:
        start_date: Start datetime
        end_date: End datetime
        user_id: User ID (defaults to default user)

    Returns:
        List of FoodLog instances
    """
    logs = await FoodLog.filter(
        user_id=user_id,
        eaten_at__gte=start_date,
        eaten_at__lte=end_date,
    ).prefetch_related("user_food")

    return logs


async def search_user_foods_by_name(
    query: str,
    user_id: UUID = DEFAULT_USER_ID,
    limit: int = 10,
) -> list[UserFood]:
    """Search user foods by name.

    Args:
        query: Search query
        user_id: User ID (defaults to default user)
        limit: Maximum number of results

    Returns:
        List of UserFood instances
    """
    foods = await UserFood.filter(
        user_id=user_id,
        name__icontains=query,
    ).limit(limit)

    return foods

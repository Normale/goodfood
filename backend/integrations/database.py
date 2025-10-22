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


def convert_nutrient_keys_to_db_format(nutrients: dict) -> dict:
    """Convert nutrient keys from kebab-case to snake_case for database.

    Args:
        nutrients: Dictionary with kebab-case keys (e.g., "vitamin-c", "total-fats", "thiamine")

    Returns:
        Dictionary with snake_case keys matching database schema (e.g., "vitamin_c", "total_fats", "vitamin_b1_thiamine")
    """
    # Mapping from NUTRIENTS config keys to database field names
    KEY_MAPPING = {
        # B vitamins - need to add vitamin_bX_ prefix
        "thiamine": "vitamin_b1_thiamine",
        "riboflavin": "vitamin_b2_riboflavin",
        "niacin": "vitamin_b3_niacin",
        "pantothenic-acid": "vitamin_b5_pantothenic_acid",
        "pyridoxine": "vitamin_b6_pyridoxine",
        "biotin": "vitamin_b7_biotin",
        "folate": "vitamin_b9_folate",
        "vitamin-b12": "vitamin_b12",

        # Other vitamins - simple conversion
        "vitamin-a": "vitamin_a",
        "vitamin-c": "vitamin_c",
        "vitamin-d": "vitamin_d",
        "vitamin-e": "vitamin_e",
        "vitamin-k": "vitamin_k",

        # Fiber - single field in config, split in DB (for now just use soluble_fiber)
        "fiber": "soluble_fiber",

        # Beneficial compounds
        "coenzyme-q10": "coq10",
        "alpha-lipoic-acid": "alpha_lipoic_acid",
        "beta-glucan": "beta_glucan",
        "resistant-starch": "resistant_starch",

        # Fats
        "total-fats": "total_fats",
        "alpha-linolenic-acid": "alpha_linolenic_acid",
        "linoleic-acid": "linoleic_acid",
        "epa-dha": "epa_dha",

        # Phytonutrients
        "beta-carotene": "beta_carotene",
        "polyphenols": "total_polyphenols",
    }

    converted = {}
    for key, value in nutrients.items():
        # Check if there's a specific mapping
        if key in KEY_MAPPING:
            db_key = KEY_MAPPING[key]
        else:
            # Default: convert kebab-case to snake_case
            db_key = key.replace("-", "_")

        converted[db_key] = value

    return converted


async def init_database() -> None:
    """Initialize database connection and run migrations."""
    logger.info("Initializing database connection...")

    # Initialize Tortoise ORM with timezone support
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models.database"]},
        timezone="UTC",  # Use UTC to avoid timezone issues
    )

    # Run migrations
    await run_migrations()

    logger.info("Database initialized successfully")


async def run_migrations() -> None:
    """Run SQL migrations."""
    logger.info("Running database migrations...")

    # Get database connection
    conn = Tortoise.get_connection("default")

    # Check if tables exist using execute_query_dict
    result = await conn.execute_query_dict(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'users'
        ) as table_exists;
        """
    )

    tables_exist = result[0]['table_exists']

    if not tables_exist:
        logger.info("Tables do not exist, running initial migration...")

        # Read and execute migration file
        migration_file = Path(__file__).parent.parent / "migrations" / "001_initial_schema.sql"
        if migration_file.exists():
            migration_sql = migration_file.read_text()
            # Execute the entire migration script at once to handle functions properly
            try:
                await conn.execute_script(migration_sql)
                logger.info("Initial migration completed")
            except Exception as e:
                logger.error(f"Migration failed: {e}")
                raise
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
        nutrients: Dictionary of nutrient values (can be kebab-case or snake_case)
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

    # Add nutrients if provided (convert keys to database format)
    if nutrients:
        converted_nutrients = convert_nutrient_keys_to_db_format(nutrients)
        food_data.update(converted_nutrients)

    food = await UserFood.create(**food_data)
    logger.info(f"Created user food: {name} (ID: {food.id})")

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


async def save_ingredients_to_cache(
    ingredients: list[dict],
) -> list[Ingredient]:
    """Save ingredient estimates to the ingredients cache table.

    This function saves individual ingredient nutritional data to the ingredients
    table for caching and future reference. It checks if each ingredient already
    exists by name before inserting.

    Args:
        ingredients: List of ingredient dictionaries, each containing:
            - ingredient_name: Name of the ingredient
            - estimates: Dictionary of nutrient values (can be kebab-case or snake_case)
            - reasoning: Optional AI reasoning about the ingredient
            - amount: Optional amount/quantity information

    Returns:
        List of created Ingredient instances (only new ingredients, not existing ones)
    """
    created_ingredients = []

    for ing_data in ingredients:
        ingredient_name = ing_data.get("ingredient_name", "")
        if not ingredient_name:
            logger.warning(f"Skipping ingredient with no name: {ing_data}")
            continue

        # Check if ingredient already exists in cache
        existing = await Ingredient.filter(name=ingredient_name).exists()

        if existing:
            logger.debug(f"Ingredient '{ingredient_name}' already exists in cache, skipping")
            continue

        # Prepare ingredient data
        ingredient_data = {
            "name": ingredient_name,
            "reasoning": ing_data.get("reasoning"),
        }

        # Add nutrient estimates if provided
        estimates = ing_data.get("estimates", {})
        if estimates:
            converted_estimates = convert_nutrient_keys_to_db_format(estimates)
            ingredient_data.update(converted_estimates)

        # Create the ingredient
        try:
            ingredient = await Ingredient.create(**ingredient_data)
            created_ingredients.append(ingredient)
            logger.info(f"Cached ingredient: {ingredient_name} (ID: {ingredient.id})")
        except Exception as e:
            logger.error(f"Failed to cache ingredient '{ingredient_name}': {e}")

    return created_ingredients

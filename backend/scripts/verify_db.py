"""Script to verify database setup and connection."""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integrations.database import init_database, close_database, get_default_user
from tortoise import Tortoise


async def verify_database():
    """Verify database connection and setup."""
    print("=" * 60)
    print("GoodFood Database Verification")
    print("=" * 60)

    try:
        # Initialize database
        print("\n1. Initializing database connection...")
        await init_database()
        print("   ✓ Database connection successful")

        # Check default user
        print("\n2. Checking default user...")
        user = await get_default_user()
        print(f"   ✓ Default user found: {user.username} (ID: {user.id})")

        # Check tables exist
        print("\n3. Verifying tables...")
        conn = Tortoise.get_connection("default")

        tables = ["users", "ingredients", "user_foods", "food_logs"]
        for table in tables:
            result = await conn.execute_query(
                f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = '{table}'
                );
                """
            )
            exists = result[0][0]
            status = "✓" if exists else "✗"
            print(f"   {status} Table '{table}' {'exists' if exists else 'missing'}")

        # Check pgvector extension
        print("\n4. Checking pgvector extension...")
        result = await conn.execute_query(
            """
            SELECT EXISTS (
                SELECT FROM pg_extension WHERE extname = 'vector'
            );
            """
        )
        vector_exists = result[0][0]
        status = "✓" if vector_exists else "✗"
        print(f"   {status} pgvector extension {'enabled' if vector_exists else 'not found'}")

        # Check trigger exists
        print("\n5. Checking nutrition vector trigger...")
        result = await conn.execute_query(
            """
            SELECT EXISTS (
                SELECT FROM pg_trigger
                WHERE tgname = 'user_foods_nutrition_vector_trigger'
            );
            """
        )
        trigger_exists = result[0][0]
        status = "✓" if trigger_exists else "✗"
        print(
            f"   {status} Nutrition vector trigger {'exists' if trigger_exists else 'missing'}"
        )

        # Check indexes
        print("\n6. Checking vector indexes...")
        indexes = [
            "idx_user_foods_nutrition_vector",
            "idx_user_foods_description_vector",
        ]
        for index in indexes:
            result = await conn.execute_query(
                f"""
                SELECT EXISTS (
                    SELECT FROM pg_indexes
                    WHERE indexname = '{index}'
                );
                """
            )
            exists = result[0][0]
            status = "✓" if exists else "✗"
            print(f"   {status} Index '{index}' {'exists' if exists else 'missing'}")

        print("\n" + "=" * 60)
        print("Database verification complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(verify_database())

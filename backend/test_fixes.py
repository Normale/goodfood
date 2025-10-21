"""Test script to verify the fixes for estimator-validator loop and database insertion."""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))


def test_nutrient_key_conversion():
    """Test that nutrient key conversion works correctly."""
    from integrations.database import convert_nutrient_keys_to_db_format

    print("=" * 80)
    print("TEST 1: Nutrient Key Conversion")
    print("=" * 80)

    # Sample nutrients from the workflow (kebab-case from NUTRIENTS config)
    sample_nutrients = {
        "calories": 500,
        "carbohydrates": 60,
        "protein": 25,
        "total-fats": 15,
        "vitamin-c": 50,
        "thiamine": 1.2,
        "riboflavin": 1.5,
        "niacin": 16,
        "pantothenic-acid": 5,
        "pyridoxine": 1.7,
        "biotin": 30,
        "folate": 400,
        "vitamin-b12": 2.4,
        "vitamin-a": 900,
        "vitamin-d": 20,
        "vitamin-e": 15,
        "vitamin-k": 120,
        "calcium": 1000,
        "iron": 18,
        "zinc": 11,
        "magnesium": 400,
        "fiber": 30,
        "alpha-linolenic-acid": 1.6,
        "linoleic-acid": 17,
        "epa-dha": 250,
        "coenzyme-q10": 100,
        "alpha-lipoic-acid": 300,
        "beta-carotene": 6,
        "polyphenols": 500,
    }

    print("\nInput nutrients (from workflow):")
    for key, value in list(sample_nutrients.items())[:5]:
        print(f"  {key}: {value}")
    print(f"  ... and {len(sample_nutrients) - 5} more")

    # Convert to database format
    converted = convert_nutrient_keys_to_db_format(sample_nutrients)

    print("\nConverted nutrients (for database):")
    for key, value in list(converted.items())[:10]:
        print(f"  {key}: {value}")
    print(f"  ... and {len(converted) - 10} more")

    # Verify specific conversions
    print("\nVerifying critical conversions:")
    tests = [
        ("total-fats", "total_fats", sample_nutrients.get("total-fats")),
        ("vitamin-c", "vitamin_c", sample_nutrients.get("vitamin-c")),
        ("thiamine", "vitamin_b1_thiamine", sample_nutrients.get("thiamine")),
        ("riboflavin", "vitamin_b2_riboflavin", sample_nutrients.get("riboflavin")),
        ("niacin", "vitamin_b3_niacin", sample_nutrients.get("niacin")),
        ("pantothenic-acid", "vitamin_b5_pantothenic_acid", sample_nutrients.get("pantothenic-acid")),
        ("coenzyme-q10", "coq10", sample_nutrients.get("coenzyme-q10")),
        ("fiber", "soluble_fiber", sample_nutrients.get("fiber")),
        ("polyphenols", "total_polyphenols", sample_nutrients.get("polyphenols")),
        ("alpha-linolenic-acid", "alpha_linolenic_acid", sample_nutrients.get("alpha-linolenic-acid")),
    ]

    all_passed = True
    for input_key, expected_db_key, expected_value in tests:
        if expected_db_key in converted and converted[expected_db_key] == expected_value:
            print(f"  [OK] '{input_key}' -> '{expected_db_key}' = {expected_value}")
        else:
            print(f"  [FAIL] '{input_key}' -> '{expected_db_key}' FAILED")
            print(f"    Expected: {expected_value}")
            print(f"    Got: {converted.get(expected_db_key, 'KEY NOT FOUND')}")
            all_passed = False

    if all_passed:
        print("\n[OK] All nutrient key conversions PASSED!")
    else:
        print("\n[FAIL] Some nutrient key conversions FAILED!")

    return all_passed


async def test_database_insertion():
    """Test that database insertion works with converted nutrients."""
    from integrations.database import create_user_food, init_database, close_database, get_default_user
    from models.database import UserFood

    print("\n" + "=" * 80)
    print("TEST 2: Database Insertion")
    print("=" * 80)

    try:
        # Initialize database
        print("\nInitializing database...")
        await init_database()
        print("[OK] Database initialized")

        # Ensure default user exists
        print("\nGetting default user...")
        user = await get_default_user()
        print(f"[OK] Default user exists: {user.username}")

        # Sample nutrients (in kebab-case format from workflow)
        sample_nutrients = {
            "calories": 350,
            "carbohydrates": 45,
            "protein": 20,
            "total-fats": 12,
            "vitamin-c": 30,
            "thiamine": 0.8,
            "riboflavin": 1.0,
            "calcium": 500,
            "iron": 10,
            "fiber": 8,
            "coenzyme-q10": 50,
        }

        print("\nCreating test user food with nutrients:")
        for key, value in sample_nutrients.items():
            print(f"  {key}: {value}")

        # Create user food
        user_food = await create_user_food(
            name="Test Meal - Grilled Chicken Salad",
            description="Test meal to verify nutrient insertion",
            nutrients=sample_nutrients,
            source="test",
        )

        print(f"\n[OK] UserFood created with ID: {user_food.id}")

        # Verify the food was saved correctly by fetching it
        print("\nFetching saved food from database...")
        saved_food = await UserFood.get(id=user_food.id)

        print(f"[OK] Food retrieved: {saved_food.name}")

        # Check that nutrients were saved
        print("\nVerifying saved nutrients:")
        checks = [
            ("calories", saved_food.calories, 350),
            ("protein", saved_food.protein, 20),
            ("total_fats", saved_food.total_fats, 12),
            ("vitamin_c", saved_food.vitamin_c, 30),
            ("vitamin_b1_thiamine", saved_food.vitamin_b1_thiamine, 0.8),
            ("vitamin_b2_riboflavin", saved_food.vitamin_b2_riboflavin, 1.0),
            ("calcium", saved_food.calcium, 500),
            ("iron", saved_food.iron, 10),
            ("soluble_fiber", saved_food.soluble_fiber, 8),
            ("coq10", saved_food.coq10, 50),
        ]

        all_passed = True
        for field_name, actual_value, expected_value in checks:
            if actual_value is not None and float(actual_value) == expected_value:
                print(f"  [OK] {field_name}: {actual_value} (expected {expected_value})")
            else:
                print(f"  [FAIL] {field_name}: {actual_value} (expected {expected_value})")
                all_passed = False

        if all_passed:
            print("\n[OK] All database nutrients SAVED correctly!")
        else:
            print("\n[FAIL] Some database nutrients FAILED to save!")

        # Cleanup test data
        print("\nCleaning up test data...")
        await saved_food.delete()
        print("[OK] Test data deleted")

        return all_passed

    except Exception as e:
        print(f"\n[FAIL] Database test FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Close database connection
        print("\nClosing database connection...")
        await close_database()
        print("[OK] Database closed")


async def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("TESTING GOODFOOD FIXES")
    print("=" * 80)

    # Test 1: Nutrient key conversion
    test1_passed = test_nutrient_key_conversion()

    # Test 2: Database insertion
    test2_passed = await test_database_insertion()

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Test 1 - Nutrient Key Conversion: {'[OK] PASSED' if test1_passed else '[FAIL] FAILED'}")
    print(f"Test 2 - Database Insertion: {'[OK] PASSED' if test2_passed else '[FAIL] FAILED'}")

    if test1_passed and test2_passed:
        print("\n[SUCCESS] All tests PASSED! The fixes are working correctly.")
        return 0
    else:
        print("\n[ERROR] Some tests FAILED. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

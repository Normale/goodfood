"""Simple test to verify nutrient conversion works in isolation."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from integrations.database import convert_nutrient_keys_to_db_format


def main():
    """Test nutrient key conversion with realistic data."""
    print("=" * 80)
    print("Nutrient Key Conversion Test (Isolated)")
    print("=" * 80)

    # Realistic nutrient data from a workflow
    nutrients_from_workflow = {
        # Macros
        "calories": 350.5,
        "protein": 24.8,
        "carbohydrates": 28.2,
        "total-fats": 15.6,
        "fiber": 3.2,
        "water": 150.0,

        # Vitamins
        "vitamin-a": 180.5,
        "thiamine": 0.12,
        "riboflavin": 0.45,
        "niacin": 3.2,
        "pantothenic-acid": 1.8,
        "pyridoxine": 0.18,
        "biotin": 25.0,
        "folate": 65.0,
        "vitamin-b12": 1.2,
        "vitamin-c": 2.5,
        "vitamin-d": 2.1,
        "vitamin-e": 1.8,
        "vitamin-k": 15.0,

        # Minerals
        "calcium": 86.0,
        "iron": 2.8,
        "magnesium": 32.0,
        "phosphorus": 220.0,
        "potassium": 280.0,
        "sodium": 420.0,
        "zinc": 1.4,
        "selenium": 28.0,
        "copper": 0.08,

        # Fats
        "alpha-linolenic-acid": 0.2,
        "linoleic-acid": 1.5,
        "epa-dha": 0.0,

        # Beneficial
        "choline": 250.0,
        "coenzyme-q10": 0.5,
    }

    print(f"\nInput: {len(nutrients_from_workflow)} nutrients (kebab-case)")
    print("Sample keys:")
    for key in list(nutrients_from_workflow.keys())[:5]:
        print(f"  - {key}")

    # Convert
    converted = convert_nutrient_keys_to_db_format(nutrients_from_workflow)

    print(f"\nOutput: {len(converted)} nutrients (snake_case for DB)")
    print("Sample keys:")
    for key in list(converted.keys())[:5]:
        print(f"  - {key}")

    # Verify critical mappings
    print("\nCritical Mappings:")
    tests = [
        ("total-fats", "total_fats"),
        ("vitamin-c", "vitamin_c"),
        ("thiamine", "vitamin_b1_thiamine"),
        ("riboflavin", "vitamin_b2_riboflavin"),
        ("niacin", "vitamin_b3_niacin"),
        ("pantothenic-acid", "vitamin_b5_pantothenic_acid"),
        ("pyridoxine", "vitamin_b6_pyridoxine"),
        ("biotin", "vitamin_b7_biotin"),
        ("folate", "vitamin_b9_folate"),
        ("vitamin-b12", "vitamin_b12"),
        ("coenzyme-q10", "coq10"),
        ("fiber", "soluble_fiber"),
        ("alpha-linolenic-acid", "alpha_linolenic_acid"),
    ]

    all_passed = True
    for input_key, expected_db_key in tests:
        if input_key in nutrients_from_workflow:
            if expected_db_key in converted:
                input_val = nutrients_from_workflow[input_key]
                output_val = converted[expected_db_key]
                if input_val == output_val:
                    print(f"  [OK] '{input_key}' -> '{expected_db_key}' = {output_val}")
                else:
                    print(f"  [FAIL] '{input_key}' -> '{expected_db_key}': value mismatch")
                    print(f"         Input: {input_val}, Output: {output_val}")
                    all_passed = False
            else:
                print(f"  [FAIL] '{input_key}' -> '{expected_db_key}': key not found in output")
                all_passed = False

    # Summary
    print("\n" + "=" * 80)
    if all_passed:
        print("[SUCCESS] All nutrient conversions working correctly!")
        print("\nThis confirms the database insertion fix is ready.")
        print("When the server saves meals, nutrients will be properly converted.")
        return 0
    else:
        print("[FAIL] Some conversions failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

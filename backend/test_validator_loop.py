"""Test the estimator-validator loop when validator rejects."""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from workflows.parallel_nutrition_workflow import create_ingredient_subgraph
from agents.ingredient_estimator import IngredientEstimator
from agents.ingredient_validator import IngredientValidator


async def test_rejection_loop():
    """Test what happens when validator rejects an estimate."""
    print("=" * 80)
    print("Testing Estimator-Validator Loop with Rejection")
    print("=" * 80)

    # Create agents
    estimator = IngredientEstimator()
    validator = IngredientValidator()

    # Create subgraph with max 3 rounds
    subgraph = create_ingredient_subgraph(estimator, validator, max_rounds=3)

    # Test with a simple ingredient
    initial_state = {
        "ingredient_name": "banana",
        "amount": "1 medium (118g)",
        "notes": None,
        "round": 0,
        "max_rounds": 3,
        "approved": False,
    }

    print(f"\nTesting with ingredient: {initial_state['ingredient_name']}")
    print(f"Amount: {initial_state['amount']}")
    print(f"Max rounds: {initial_state['max_rounds']}")
    print("\nRunning workflow...")
    print("-" * 80)

    try:
        # Run the subgraph
        result = await asyncio.wait_for(subgraph.ainvoke(initial_state), timeout=120.0)

        print("\n" + "=" * 80)
        print("Result:")
        print("=" * 80)
        print(f"Approved: {result.get('approved')}")
        print(f"Final round: {result.get('round')}")
        print(f"Confidence: {result.get('confidence_level')}")
        print(f"Feedback: {result.get('feedback', 'None')}")

        if result.get('estimates'):
            estimates = result['estimates']
            print(f"\nFinal estimates (showing first 5):")
            for i, (nutrient, value) in enumerate(list(estimates.items())[:5]):
                print(f"  {nutrient}: {value}")

        # Check if it completed
        if result.get('approved'):
            print("\n[OK] Workflow completed successfully")
            return True
        else:
            print("\n[FAIL] Workflow did not reach approval")
            return False

    except asyncio.TimeoutError:
        print("\n[FAIL] Workflow timed out after 120 seconds")
        print("This suggests the loop is hanging!")
        return False
    except Exception as e:
        print(f"\n[FAIL] Workflow failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run the test."""
    result = await test_rejection_loop()

    print("\n" + "=" * 80)
    if result:
        print("[SUCCESS] The estimator-validator loop is working!")
    else:
        print("[FAIL] The estimator-validator loop has issues")

    return 0 if result else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

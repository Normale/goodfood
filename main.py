"""GoodFood - Nutrition estimation from meal descriptions."""

import asyncio
from datetime import datetime

from src.database.gateway import DatabaseGateway
from src.models.nutrition import MealType
from src.workflows.estimation_workflow import EstimationWorkflow


async def estimate_and_save(description: str, meal_type: str = "dinner"):
    """Estimate nutrients and save to database.

    Args:
        description: Natural language meal description
        meal_type: Type of meal (breakfast/lunch/dinner/snack)
    """
    # Run estimation workflow
    workflow = EstimationWorkflow()
    result = await workflow.run(description)

    # Save to database
    db = DatabaseGateway()

    record = await db.save_nutrition(
        name=description[:100],  # Use first 100 chars as name
        description=description,
        meal_type=MealType(meal_type.lower()),
        nutrients=result["estimates"],
        timestamp=datetime.now(),
    )

    print(f"\nSaved to database!")
    print(f"   ID: {record.id}")
    print(f"   Protein: {record.protein}g")
    print(f"   Carbs: {record.carbohydrates}g")
    print(f"   Fats: {record.total_fats}g")


async def show_history():
    """Show recent nutrition history."""
    db = DatabaseGateway()
    records = await db.get_history(limit=10)

    print(f"\nRecent meals ({len(records)}):")
    for record in records:
        print(f"\n   {record.name}")
        print(f"   {record.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print(f"   P: {record.protein}g | C: {record.carbohydrates}g | F: {record.total_fats}g")


async def main():
    """Main entry point."""
    print("GoodFood - Nutrition Estimation from Descriptions\n")

    # Example: Estimate from description
    description = "Grilled chicken breast 200g with brown rice 150g and steamed broccoli 100g"

    await estimate_and_save(description, meal_type="dinner")

    # Show history
    await show_history()


if __name__ == "__main__":
    asyncio.run(main())

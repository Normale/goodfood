"""Main FastAPI server with WebSocket for nutrition estimation."""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from integrations.database import (
    close_database,
    create_user_food,
    get_default_user,
    get_food_logs_by_date_range,
    init_database,
    log_food,
    save_ingredients_to_cache,
)
from workflows.gap_analysis_workflow import GapAnalysisWorkflow
from workflows.parallel_nutrition_workflow import ParallelNutritionWorkflow

app = FastAPI(title="GoodFood Nutrition API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: List[WebSocket] = []


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    await init_database()
    await get_default_user()  # Ensure default user exists
    print("Database initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown."""
    await close_database()
    print("Database connections closed")


async def broadcast_update(component: str, data: dict):
    """Broadcast update to all connected clients."""
    message = {"component": component, "data": data}

    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Error sending to client: {e}")


async def get_todays_meals() -> List[dict]:
    """Get today's meals from database."""
    # Get start and end of today (UTC timezone-aware)
    now = datetime.now(timezone.utc)
    start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)

    # Fetch today's food logs from database
    food_logs = await get_food_logs_by_date_range(start_of_day, end_of_day)

    # Convert to the format expected by the frontend
    meals = []
    for log in food_logs:
        food = log.user_food

        # Build detailed nutrients dict
        detailed_nutrients = {
            "carbohydrates": float(food.carbohydrates or 0),
            "protein": float(food.protein or 0),
            "total_fats": float(food.total_fats or 0),
            "alpha_linolenic_acid": float(food.alpha_linolenic_acid or 0),
            "linoleic_acid": float(food.linoleic_acid or 0),
            "epa_dha": float(food.epa_dha or 0),
            "soluble_fiber": float(food.soluble_fiber or 0),
            "insoluble_fiber": float(food.insoluble_fiber or 0),
            "water": float(food.water or 0),
            "vitamin_c": float(food.vitamin_c or 0),
            "vitamin_b1_thiamine": float(food.vitamin_b1_thiamine or 0),
            "vitamin_b2_riboflavin": float(food.vitamin_b2_riboflavin or 0),
            "vitamin_b3_niacin": float(food.vitamin_b3_niacin or 0),
            "vitamin_b5_pantothenic_acid": float(food.vitamin_b5_pantothenic_acid or 0),
            "vitamin_b6_pyridoxine": float(food.vitamin_b6_pyridoxine or 0),
            "vitamin_b7_biotin": float(food.vitamin_b7_biotin or 0),
            "vitamin_b9_folate": float(food.vitamin_b9_folate or 0),
            "vitamin_b12": float(food.vitamin_b12 or 0),
            "vitamin_a": float(food.vitamin_a or 0),
            "vitamin_d": float(food.vitamin_d or 0),
            "vitamin_e": float(food.vitamin_e or 0),
            "vitamin_k": float(food.vitamin_k or 0),
            "calcium": float(food.calcium or 0),
            "phosphorus": float(food.phosphorus or 0),
            "magnesium": float(food.magnesium or 0),
            "potassium": float(food.potassium or 0),
            "sodium": float(food.sodium or 0),
            "chloride": float(food.chloride or 0),
            "iron": float(food.iron or 0),
            "zinc": float(food.zinc or 0),
            "copper": float(food.copper or 0),
            "selenium": float(food.selenium or 0),
            "manganese": float(food.manganese or 0),
            "iodine": float(food.iodine or 0),
            "chromium": float(food.chromium or 0),
            "molybdenum": float(food.molybdenum or 0),
            "leucine": float(food.leucine or 0),
            "lysine": float(food.lysine or 0),
            "valine": float(food.valine or 0),
            "isoleucine": float(food.isoleucine or 0),
            "threonine": float(food.threonine or 0),
            "methionine": float(food.methionine or 0),
            "phenylalanine": float(food.phenylalanine or 0),
            "histidine": float(food.histidine or 0),
            "tryptophan": float(food.tryptophan or 0),
            "choline": float(food.choline or 0),
            "taurine": float(food.taurine or 0),
            "coq10": float(food.coq10 or 0),
            "alpha_lipoic_acid": float(food.alpha_lipoic_acid or 0),
            "beta_glucan": float(food.beta_glucan or 0),
            "resistant_starch": float(food.resistant_starch or 0),
            "beta_carotene": float(food.beta_carotene or 0),
            "lycopene": float(food.lycopene or 0),
            "lutein": float(food.lutein or 0),
            "zeaxanthin": float(food.zeaxanthin or 0),
            "total_polyphenols": float(food.total_polyphenols or 0),
            "quercetin": float(food.quercetin or 0),
            "sulforaphane": float(food.sulforaphane or 0),
            "allicin": float(food.allicin or 0),
            "curcumin": float(food.curcumin or 0),
        }

        meal = {
            "id": str(log.id),
            "time": log.eaten_at.strftime("%I:%M %p"),
            "description": food.name,
            "calories": float(food.calories or 0),
            "protein": float(food.protein or 0),
            "carbs": float(food.carbohydrates or 0),
            "fat": float(food.total_fats or 0),
            "detailed_nutrients": detailed_nutrients,
        }
        meals.append(meal)

    return meals


async def run_gap_analysis(websocket=None) -> Dict:
    """Run gap analysis workflow on today's meals.

    Args:
        websocket: Optional WebSocket for streaming progress

    Returns:
        Gap analysis results
    """
    meals = await get_todays_meals()
    workflow = GapAnalysisWorkflow()
    result = await workflow.analyze_gaps(meals, websocket)
    return result


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for bidirectional communication."""
    await websocket.accept()
    active_connections.append(websocket)

    print(f"Client connected. Total connections: {len(active_connections)}")

    try:
        # Send initial data to newly connected client
        todays_meals = await get_todays_meals()
        await websocket.send_json({"component": "todaysMeals", "data": todays_meals})

        # Only run gap analysis if there are meals
        if todays_meals:
            gap_analysis_result = await run_gap_analysis(websocket)

            # Send gap analysis results - send the full gap objects, not just current values
            top_gaps = gap_analysis_result.get("top_gaps", [])
            await websocket.send_json({"component": "nutrientGaps", "data": top_gaps})

            # Send meal suggestions (first one for NextMealSuggestion component)
            meal_suggestions = gap_analysis_result.get("meal_suggestions", [])
            if meal_suggestions:
                await websocket.send_json(
                    {"component": "recommendedMeal", "data": meal_suggestions[0]}
                )
            else:
                await websocket.send_json(
                    {
                        "component": "recommendedMeal",
                        "data": {
                            "meal": "Add your first meal to get personalized suggestions",
                            "reasoning": "Track meals to receive nutrition guidance",
                        },
                    }
                )
        else:
            # No meals yet
            await websocket.send_json({"component": "nutrientGaps", "data": []})
            await websocket.send_json(
                {
                    "component": "recommendedMeal",
                    "data": {
                        "meal": "Start by adding your first meal",
                        "reasoning": "Track meals to get personalized nutrition insights",
                    },
                }
            )

        # Listen for messages from client
        while True:
            message = await websocket.receive_json()
            print(f"Received message: {message}")
            # Handle meal input with nutrition estimation
            if message.get("action") == "add_meal":
                meal_text = message.get("text", "")
                print(f"Estimating nutrition for: {meal_text}")

                # Use parallel nutrition workflow to estimate
                workflow = ParallelNutritionWorkflow(max_rounds_per_ingredient=3)
                result = await workflow.estimate_meal(meal_text, websocket)

                # Prepare nutrients dictionary from estimates
                estimates = result.get("estimates", {})
                nutrients = {
                    "calories": result.get("calories", 0),
                    "carbohydrates": result.get("carbs", 0),
                    "protein": result.get("protein", 0),
                    "total_fats": result.get("fat", 0),
                }

                # Add all detailed nutrients from estimates
                nutrients.update(estimates)

                # Save individual ingredients to cache
                ingredient_results = result.get("ingredient_results", {})
                if ingredient_results:
                    # Convert ingredient_results dict to list format
                    ingredients_list = list(ingredient_results.values())
                    await save_ingredients_to_cache(ingredients_list)

                # Create user food in database
                user_food = await create_user_food(
                    name=meal_text,
                    description=meal_text,
                    nutrients=nutrients,
                )

                # Log the food consumption
                await log_food(
                    user_food_id=user_food.id,
                    meal_type=None,  # Could be determined from time of day
                )

                # Broadcast updated meals list
                updated_meals = await get_todays_meals()
                await broadcast_update("todaysMeals", updated_meals)

                # Run gap analysis workflow with updated meals
                print("Running gap analysis...")
                gap_analysis_result = await run_gap_analysis(websocket)

                # Broadcast gap analysis results - send full gap objects
                top_gaps = gap_analysis_result.get("top_gaps", [])
                await broadcast_update("nutrientGaps", top_gaps)

                # Broadcast meal suggestion (first one)
                meal_suggestions = gap_analysis_result.get("meal_suggestions", [])
                if meal_suggestions:
                    await broadcast_update("recommendedMeal", meal_suggestions[0])
                else:
                    await broadcast_update(
                        "recommendedMeal",
                        {
                            "meal": "Balanced meal with protein and vegetables",
                            "reasoning": "Helps meet daily nutritional goals",
                        },
                    )

                print(f"Broadcasted updates to {len(active_connections)} clients")

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"Client disconnected. Total connections: {len(active_connections)}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "active_connections": len(active_connections)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

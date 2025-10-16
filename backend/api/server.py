"""Main FastAPI server with WebSocket for nutrition estimation."""

import asyncio
from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from workflows.nutrition_langgraph import NutritionEstimationWorkflow
from workflows.parallel_nutrition_workflow import ParallelNutritionWorkflow
from workflows.gap_analysis_workflow import GapAnalysisWorkflow

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

# Store today's meals in memory (in production, use a database)
todays_meals: List[Dict] = []


async def broadcast_update(component: str, data: dict):
    """Broadcast update to all connected clients."""
    message = {"component": component, "data": data}

    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Error sending to client: {e}")


def get_todays_meals() -> List[dict]:
    """Get today's meals list."""
    return todays_meals


async def run_gap_analysis(websocket=None) -> Dict:
    """Run gap analysis workflow on today's meals.

    Args:
        websocket: Optional WebSocket for streaming progress

    Returns:
        Gap analysis results
    """
    workflow = GapAnalysisWorkflow()
    result = await workflow.analyze_gaps(todays_meals, websocket)
    return result


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for bidirectional communication."""
    await websocket.accept()
    active_connections.append(websocket)

    print(f"Client connected. Total connections: {len(active_connections)}")

    try:
        # Send initial data to newly connected client
        await websocket.send_json({"component": "todaysMeals", "data": get_todays_meals()})

        # Only run gap analysis if there are meals
        if todays_meals:
            gap_analysis_result = await run_gap_analysis(websocket)

            # Send gap analysis results - send the full gap objects, not just current values
            top_gaps = gap_analysis_result.get("top_gaps", [])
            await websocket.send_json({"component": "nutrientGaps", "data": top_gaps})

            # Send meal suggestions (first one for NextMealSuggestion component)
            meal_suggestions = gap_analysis_result.get("meal_suggestions", [])
            if meal_suggestions:
                await websocket.send_json({
                    "component": "recommendedMeal",
                    "data": meal_suggestions[0]
                })
            else:
                await websocket.send_json({
                    "component": "recommendedMeal",
                    "data": {
                        "meal": "Add your first meal to get personalized suggestions",
                        "reasoning": "Track meals to receive nutrition guidance"
                    }
                })
        else:
            # No meals yet
            await websocket.send_json({"component": "nutrientGaps", "data": []})
            await websocket.send_json({
                "component": "recommendedMeal",
                "data": {
                    "meal": "Start by adding your first meal",
                    "reasoning": "Track meals to get personalized nutrition insights"
                }
            })

        # Listen for messages from client
        while True:
            message = await websocket.receive_json()

            # Handle meal input with nutrition estimation
            if message.get("action") == "add_meal":
                meal_text = message.get("text", "")
                print(f"Estimating nutrition for: {meal_text}")

                # Use parallel nutrition workflow to estimate
                workflow = ParallelNutritionWorkflow(max_rounds_per_ingredient=3)
                result = await workflow.estimate_meal(meal_text, websocket)

                # Create new meal with estimated nutrition
                new_meal = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "time": datetime.now().strftime("%I:%M %p"),
                    "description": meal_text,
                    "calories": result.get("calories", 0),
                    "protein": result.get("protein", 0),
                    "carbs": result.get("carbs", 0),
                    "fat": result.get("fat", 0),
                    "detailed_nutrients": result.get("estimates", {}),
                }

                # Add to today's meals
                todays_meals.append(new_meal)

                # Broadcast updated meals list
                await broadcast_update("todaysMeals", get_todays_meals())

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
                    await broadcast_update("recommendedMeal", {
                        "meal": "Balanced meal with protein and vegetables",
                        "reasoning": "Helps meet daily nutritional goals"
                    })

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

"""Main FastAPI server with WebSocket for nutrition estimation."""

import asyncio
from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.src.workflows.nutrition_workflow import NutritionEstimationWorkflow

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


async def broadcast_update(component: str, data: dict):
    """Broadcast update to all connected clients."""
    message = {"component": component, "data": data}

    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception as e:
            print(f"Error sending to client: {e}")


def get_initial_meals() -> List[dict]:
    """Get initial meals list."""
    return [
        {
            "id": 1,
            "time": "8:30 AM",
            "description": "Oatmeal with berries, banana, and almond butter",
            "calories": 420,
            "protein": 12,
            "carbs": 68,
            "fat": 14,
        },
        {
            "id": 2,
            "time": "12:45 PM",
            "description": "Grilled chicken salad with quinoa and avocado",
            "calories": 580,
            "protein": 42,
            "carbs": 45,
            "fat": 22,
        },
        {
            "id": 3,
            "time": "3:15 PM",
            "description": "Greek yogurt with honey and walnuts",
            "calories": 280,
            "protein": 15,
            "carbs": 32,
            "fat": 11,
        },
    ]


def get_nutrient_gaps() -> dict:
    """Get nutrient gaps data."""
    return {
        "vitamin_d": 8,
        "fiber": 15,
        "iron": 12,
        "calcium": 500,
        "vitamin_b12": 1.5,
        "omega_3": 0.8,
    }


def get_recommended_meal() -> dict:
    """Get recommended next meal."""
    return {
        "meal": "Salmon with quinoa and roasted vegetables",
        "reasoning": "High in protein and omega-3s, adds fiber from quinoa and veggies",
        "nutrients": {
            "calories": 520,
            "protein": 38,
            "carbs": 45,
            "fat": 18,
            "omega_3": 2.5,
            "vitamin_d": 12,
        },
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for bidirectional communication."""
    await websocket.accept()
    active_connections.append(websocket)

    print(f"Client connected. Total connections: {len(active_connections)}")

    try:
        # Send initial data to newly connected client
        await websocket.send_json({"component": "todaysMeals", "data": get_initial_meals()})
        await websocket.send_json({"component": "nutrientGaps", "data": get_nutrient_gaps()})
        await websocket.send_json({"component": "recommendedMeal", "data": get_recommended_meal()})

        # Listen for messages from client
        while True:
            message = await websocket.receive_json()

            # Handle meal input with nutrition estimation
            if message.get("action") == "add_meal":
                meal_text = message.get("text", "")
                print(f"Estimating nutrition for: {meal_text}")

                # Use nutrition workflow to estimate
                workflow = NutritionEstimationWorkflow()
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

                # Get current meals and add new one
                current_meals = get_initial_meals()
                current_meals.append(new_meal)

                # Broadcast updated meals list
                await broadcast_update("todaysMeals", current_meals)
                await broadcast_update("nutrientGaps", get_nutrient_gaps())
                await broadcast_update("recommendedMeal", get_recommended_meal())

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

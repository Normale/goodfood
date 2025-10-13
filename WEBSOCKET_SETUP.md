# WebSocket Setup - Simple UI Updates

This is a simplified setup for testing WebSocket-based component updates between the FastAPI backend and React frontend.

## How It Works

1. **Backend** (`simple_server.py`):
   - WebSocket server at `ws://localhost:8000/ws`
   - `add_today(text: str)` - Fake function that always returns the same meal
   - Broadcasts JSON updates to specific components:
     - `todaysMeals` - Updates the meals list
     - `nutrientGaps` - Updates top nutrient gaps
     - `recommendedMeal` - Updates recommended next meal

2. **Frontend** (`frontend/src/App.jsx`):
   - Connects to WebSocket on mount
   - Listens for component-specific updates
   - Routes updates to appropriate React state

## Running the System

### Terminal 1 - Backend
```bash
# From project root
python simple_server.py
```

Backend will start on `http://localhost:8000`

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Frontend will start on `http://localhost:5173`

## Testing the Flow

1. Open browser to `http://localhost:5173`
2. Open browser console (F12) to see WebSocket messages
3. Type any text in "What did you eat today?" input
4. Click "Log Meal"
5. Watch the UI components update automatically via WebSocket

## Message Format

### Client → Server
```json
{
  "action": "add_meal",
  "text": "Grilled chicken with rice"
}
```

### Server → Client
```json
{
  "component": "todaysMeals",
  "data": [
    {
      "id": 1,
      "time": "8:30 AM",
      "description": "...",
      "calories": 420,
      "protein": 12,
      "carbs": 68,
      "fat": 14
    }
  ]
}
```

## Components Updated

1. **Today's Meals** (`todaysMeals`)
   - List of all meals for the day
   - Automatically recalculates daily totals

2. **Nutrient Gaps** (`nutrientGaps`)
   - Shows deficient nutrients
   - Format: `{ vitamin_d: 8, fiber: 15, ... }`

3. **Recommended Meal** (`recommendedMeal`)
   - Suggested next meal
   - Format: `{ meal: "...", reasoning: "...", nutrients: {...} }`

## Next Steps (Future)

- Replace `add_today()` with actual AI estimation workflow
- Add user authentication and per-user meal history
- Connect to PostgreSQL database
- Add real-time multi-user sync

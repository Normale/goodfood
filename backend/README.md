# GoodFood Backend

Comprehensive nutrition tracking and estimation system powered by AI agents.

## Architecture

```
backend/
├── main.py                 # Entry point for the server
├── src/
│   ├── api/               # API endpoints and WebSocket handlers
│   │   └── server.py      # Main FastAPI server
│   ├── agents/            # AI agents for nutrition analysis
│   │   ├── input_agent.py          # Basic input processing
│   │   ├── input_critic.py         # Basic verification
│   │   ├── nutrition_estimator.py  # Comprehensive nutrition estimator
│   │   └── nutrition_verifier.py   # Comprehensive nutrition verifier
│   ├── workflows/         # Business logic workflows
│   │   ├── estimation_workflow.py  # Basic estimation workflow
│   │   └── nutrition_workflow.py   # Comprehensive nutrition workflow
│   ├── config/            # Configuration and settings
│   ├── database/          # Database models and operations
│   ├── models/            # Data models
│   ├── integrations/      # External API integrations
│   └── utils/             # Utility functions
```

## Key Components

### Agents

**NutritionEstimatorAgent** (`agents/nutrition_estimator.py`)
- Estimates comprehensive nutritional content from meal descriptions
- Tracks 70+ nutrients including:
  - Macronutrients (protein, carbs, fats, fiber, water)
  - Vitamins (all B vitamins, A, C, D, E, K)
  - Minerals (calcium, iron, zinc, selenium, etc.)
  - Essential amino acids
  - Beneficial compounds (choline, CoQ10, taurine)
  - Phytonutrients (polyphenols, carotenoids, etc.)

**NutritionVerifierAgent** (`agents/nutrition_verifier.py`)
- Validates estimates for accuracy
- Identifies values that are significantly off (>25% deviation)
- Provides detailed feedback for refinement
- Calculates approval percentage

### Workflows

**NutritionEstimationWorkflow** (`workflows/nutrition_workflow.py`)
- Coordinates estimator and verifier agents
- Iterative refinement process (up to 5 iterations)
- Streams progress updates via WebSocket
- Returns estimates when 80%+ approval reached

### API

**FastAPI Server** (`api/server.py`)
- WebSocket endpoint for real-time communication
- Handles meal additions with nutrition estimation
- Broadcasts updates to all connected clients
- Health check endpoint

## Running the Backend

### Development

```bash
# From the repository root
cd backend
python main.py
```

Server will start on `http://0.0.0.0:8000`

### Production

```bash
uvicorn backend.src.api.server:app --host 0.0.0.0 --port 8000
```

## WebSocket API

### Connection

Connect to: `ws://localhost:8000/ws`

### Messages

**Client → Server:**
```json
{
  "action": "add_meal",
  "text": "Grilled salmon with quinoa and broccoli"
}
```

**Server → Client (Progress Updates):**
```json
{
  "type": "workflow_start",
  "description": "Grilled salmon...",
  "max_iterations": 5
}

{
  "type": "iteration",
  "iteration": 1,
  "max": 5
}

{
  "type": "status",
  "status": "estimating",
  "message": "Analyzing meal..."
}

{
  "type": "estimates",
  "macros": {
    "calories": 520,
    "protein": 38,
    "carbs": 45,
    "fat": 18
  },
  "confidence": "high",
  "full_count": 70
}

{
  "type": "consensus",
  "message": "Consensus reached! (85% approval)",
  "iterations": 2
}
```

**Server → Client (Component Updates):**
```json
{
  "component": "todaysMeals",
  "data": [...]
}

{
  "component": "nutrientGaps",
  "data": {...}
}

{
  "component": "recommendedMeal",
  "data": {...}
}
```

## Environment Variables

Create a `.env` file in the repository root:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Features

- **Real-time Estimation**: Live nutrition analysis as users input meals
- **Iterative Refinement**: Estimator and verifier agents work together to improve accuracy
- **Comprehensive Tracking**: 70+ nutrients tracked for each meal
- **WebSocket Streaming**: Real-time progress updates during estimation
- **Multi-client Support**: Broadcasts updates to all connected clients
- **Error Handling**: Graceful degradation if estimation fails

## Future Enhancements

- Database persistence for meals and user profiles
- Historical nutrition trends and analytics
- Personalized recommendations based on dietary goals
- Integration with nutrition databases (USDA, OpenFoodFacts)
- Meal planning and recipe suggestions
- Export functionality (PDF, CSV)

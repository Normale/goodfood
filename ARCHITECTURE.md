# GoodFood Architecture

## Overview

GoodFood is a comprehensive nutrition tracking application with a React frontend and Python backend powered by AI agents for accurate nutrition estimation.

## Repository Structure

```
goodfood/
├── backend/                    # Python backend (NEW)
│   ├── main.py                # Server entry point
│   ├── src/
│   │   ├── api/              # FastAPI server & WebSocket handlers
│   │   ├── agents/           # AI agents for nutrition analysis
│   │   ├── workflows/        # Business logic workflows
│   │   ├── config/           # Configuration
│   │   ├── database/         # Database models
│   │   ├── models/           # Data models
│   │   ├── integrations/     # External APIs
│   │   └── utils/            # Utilities
│   └── README.md             # Backend documentation
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.jsx           # Main app
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── alembic/                   # Database migrations
├── scripts/                   # Utility scripts
├── .env                       # Environment variables
├── pyproject.toml            # Python dependencies
├── docker-compose.yml        # Docker configuration
└── README.md                 # Main documentation
```

## Key Components

### Backend

The backend is organized into a clean, modular architecture:

**API Layer** (`backend/src/api/`)
- FastAPI server with WebSocket support
- Real-time bidirectional communication
- CORS configured for frontend

**Agents** (`backend/src/agents/`)
- `NutritionEstimatorAgent`: Estimates 70+ nutrients from meal descriptions
- `NutritionVerifierAgent`: Validates estimates and provides feedback
- Iterative refinement through agent collaboration

**Workflows** (`backend/src/workflows/`)
- `NutritionEstimationWorkflow`: Orchestrates estimator/verifier agents
- Streams progress updates to frontend
- Achieves consensus through multiple iterations

**Configuration** (`backend/src/config/`)
- Settings management
- Environment variable handling

**Database** (`backend/src/database/`)
- SQLAlchemy models
- Database operations

### Frontend

React application built with Vite:

**Components** (`frontend/src/components/`)
- `NextMealSuggestion`: Displays AI-recommended meals
- `TodaysMeals`: Shows logged meals with nutrition
- `NutrientGaps`: Visualizes nutrient deficiencies
- UI components library

**WebSocket Integration**
- Real-time updates from backend
- Progress streaming during estimation
- Automatic reconnection

## Data Flow

### Meal Addition Flow

1. User enters meal description in frontend
2. Frontend sends via WebSocket: `{"action": "add_meal", "text": "..."}`
3. Backend initiates `NutritionEstimationWorkflow`
4. **Iteration Loop** (up to 5 times):
   - `NutritionEstimatorAgent` analyzes meal → estimates 70+ nutrients
   - Frontend receives progress: `{"type": "estimating", ...}`
   - `NutritionVerifierAgent` validates estimates → provides feedback
   - Frontend receives: `{"type": "verification", "approval": 75, ...}`
   - If approval < 80%, loop continues with feedback
5. Consensus reached (80%+ approval)
6. Backend creates meal entry with nutrition data
7. Backend broadcasts updates to all connected clients:
   - Updated meals list
   - Updated nutrient gaps
   - New meal recommendation
8. Frontend updates UI components

### Component Updates Flow

```
Backend → WebSocket → Frontend
         ↓
    {component: "todaysMeals", data: [...]}
    {component: "nutrientGaps", data: {...}}
    {component: "recommendedMeal", data: {...}}
         ↓
    React State Update
         ↓
    UI Re-render
```

## Technology Stack

### Backend
- **FastAPI**: Modern web framework
- **Anthropic Claude**: AI for nutrition estimation
- **SQLAlchemy**: ORM for database
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **WebSockets**: Real-time communication

### Frontend
- **React**: UI framework
- **Vite**: Build tool
- **Framer Motion**: Animations
- **WebSocket API**: Real-time updates

### Infrastructure
- **Docker**: Containerization
- **PostgreSQL**: Database
- **uvicorn**: ASGI server

## Running the Application

### Backend

```bash
# From repository root
.venv/Scripts/python.exe backend/main.py

# Or with uvicorn directly
uvicorn backend.src.api.server:app --reload
```

Server runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### Docker (Full Stack)

```bash
docker-compose up
```

## Environment Variables

Create `.env` in repository root:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional
DATABASE_URL=postgresql://user:pass@localhost/goodfood
ENVIRONMENT=development
LOG_LEVEL=info
```

## API Endpoints

### WebSocket
- `ws://localhost:8000/ws` - Main bidirectional communication

### HTTP
- `GET /health` - Health check

## Agent System

### Nutrition Estimator

**Input**: Meal description (natural language)

**Process**:
1. Parse ingredients and quantities
2. Estimate 70+ nutrients using Claude
3. Calculate macros and micronutrients
4. Provide confidence level and assumptions

**Output**:
```json
{
  "estimates": {
    "Protein (g)": 38,
    "Carbohydrates (g)": 45,
    "Total Fats (g)": 18,
    "Vitamin C (mg)": 85,
    ...
  },
  "confidence_level": "high",
  "reasoning": "...",
  "assumptions": [...]
}
```

### Nutrition Verifier

**Input**: Meal description + estimates

**Process**:
1. Validate each nutrient estimate
2. Identify significant deviations (>25%)
3. Provide specific feedback
4. Calculate approval percentage

**Output**:
```json
{
  "approved": true/false,
  "approval_percentage": 85,
  "issues_found": [...],
  "feedback": "...",
  "overall_feedback": "..."
}
```

## Development Workflow

### Adding New Agents

1. Create agent class in `backend/src/agents/`
2. Implement required methods
3. Add to workflow in `backend/src/workflows/`
4. Update API endpoints if needed

### Adding New Workflows

1. Create workflow class in `backend/src/workflows/`
2. Coordinate multiple agents
3. Handle WebSocket streaming
4. Update server to use new workflow

### Database Changes

1. Modify models in `backend/src/database/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

## Testing

```bash
# Backend tests (TODO)
pytest backend/tests/

# Frontend tests (TODO)
cd frontend && npm test
```

## Deployment Considerations

- Use environment variables for secrets
- Configure CORS for production domains
- Use PostgreSQL in production
- Enable SSL for WebSocket connections
- Implement rate limiting
- Add authentication/authorization
- Monitor API usage and costs

## Future Enhancements

### Backend
- [ ] User authentication and profiles
- [ ] Historical meal storage
- [ ] Nutrient trend analytics
- [ ] Integration with nutrition databases (USDA, OpenFoodFacts)
- [ ] Meal planning engine
- [ ] Recipe suggestions
- [ ] Export functionality

### Frontend
- [ ] User dashboard
- [ ] Nutrition charts and graphs
- [ ] Meal history view
- [ ] Goal setting and tracking
- [ ] Offline support
- [ ] Mobile app (React Native)

### Infrastructure
- [ ] Caching layer (Redis)
- [ ] Message queue (Celery)
- [ ] Monitoring (Prometheus/Grafana)
- [ ] CI/CD pipeline
- [ ] Load balancing
- [ ] Horizontal scaling

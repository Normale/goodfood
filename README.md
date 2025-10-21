# 🍽️ GoodFood - AI-Powered Nutrition Tracking

Comprehensive nutrition tracking with AI-powered estimation. Just describe what you ate, and agents estimate 70+ nutrients with iterative refinement.

## Features

- **Natural Language Input**: Describe meals in plain English
- **Comprehensive Tracking**: 70+ nutrients (macros, vitamins, minerals, amino acids, phytonutrients)
- **Iterative Refinement**: Estimator and verifier agents collaborate for accuracy
- **Real-Time WebSocket**: Live progress updates during estimation
- **React Frontend**: Modern UI with nutrition visualization

## Quick Start

See [QUICKSTART.md](./QUICKSTART.md) for a 5-minute getting started guide.

### Backend

```bash
# Install dependencies
uv sync

# Set up environment
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY

# Run server
python backend/main.py
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

Starts backend and frontend.

## Architecture

```
goodfood/
├── backend/                    # Python backend
│   ├── main.py                # Entry point
│   ├── src/
│   │   ├── api/              # FastAPI + WebSocket
│   │   ├── agents/           # AI agents (estimator, verifier)
│   │   ├── workflows/        # Orchestration logic
│   │   ├── config/           # Settings
│   │   ├── models/           # Data models
│   │   └── integrations/     # External APIs
│   └── README.md
├── frontend/                  # React frontend
│   └── src/
│       ├── components/       # UI components
│       └── App.jsx
└── docs/
    ├── ARCHITECTURE.md       # Detailed architecture
    └── QUICKSTART.md         # Getting started
```

For detailed architecture, see [ARCHITECTURE.md](./ARCHITECTURE.md)

## How It Works

### 1. User Input
User describes a meal: "Grilled salmon with quinoa and broccoli"

### 2. AI Estimation
**NutritionEstimatorAgent** analyzes the description:
- Parses ingredients and quantities
- Estimates 70+ nutrients
- Provides confidence level and assumptions

### 3. Verification
**NutritionVerifierAgent** validates estimates:
- Checks each nutrient for accuracy
- Identifies values that are significantly off (>25% deviation)
- Provides detailed feedback

### 4. Iterative Refinement
Agents collaborate (up to 5 iterations):
```
Iteration 1:
  → Estimator: protein=38g, carbs=45g, vitamin_c=85mg...
  → Verifier: "Approval 75% - vitamin C seems high for this meal"

Iteration 2:
  → Estimator: (adjusts) vitamin_c=60mg...
  → Verifier: "Approval 85% - looks good"

✅ Consensus reached (85% approval)!
```

### 5. Real-Time Updates
Progress streamed to frontend via WebSocket:
- Current iteration
- Estimation phase
- Verification results
- Final consensus

### 6. Display
Meal displayed in UI with complete nutritional profile.

## Nutrients Tracked

**70+ nutrients** across all categories:

### Macronutrients (9)
Protein, Carbohydrates, Total Fats, Fiber (soluble/insoluble), Essential fatty acids, Water

### Vitamins (13)
All B vitamins (B1-B12), Vitamins A, C, D, E, K

### Minerals (14)
Calcium, Iron, Magnesium, Zinc, Selenium, Potassium, Sodium, and more

### Essential Amino Acids (9)
Leucine, Lysine, Valine, Isoleucine, Threonine, and more

### Beneficial Compounds (6)
Choline, Taurine, CoQ10, Alpha-lipoic acid, Beta-glucan, Resistant starch

### Phytonutrients (9)
Beta-carotene, Lycopene, Polyphenols, Quercetin, and more

## API

### WebSocket Endpoint
`ws://localhost:8000/ws`

**Client → Server:**
```json
{
  "action": "add_meal",
  "text": "Grilled salmon with quinoa and broccoli"
}
```

**Server → Client (Progress):**
```json
{"type": "workflow_start", "description": "...", "max_iterations": 5}
{"type": "iteration", "iteration": 1, "max": 5}
{"type": "status", "status": "estimating", "message": "Analyzing meal..."}
{"type": "estimates", "macros": {...}, "confidence": "high"}
{"type": "verification", "approval": 85, "issues_count": 2}
{"type": "consensus", "message": "Consensus reached!"}
```

### HTTP Endpoints
- `GET /health` - Health check

## Configuration

`.env` file:
```env
# Required
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional (with defaults)
OPENFOODFACTS_MCP_URL=http://localhost:3000
MAX_ITERATIONS=5
APPROVAL_THRESHOLD=80
CONFIDENCE_THRESHOLD=0.7
ESTIMATOR_MODEL=claude-3-5-haiku-latest
CRITIC_MODEL=claude-3-5-haiku-latest
LOG_LEVEL=INFO
```

## Technologies

**Backend:**
- FastAPI - Web framework
- Anthropic Claude - AI for nutrition estimation
- WebSockets - Real-time communication

**Frontend:**
- React - UI framework
- Vite - Build tool
- Framer Motion - Animations

**Infrastructure:**
- Docker - Containerization
- uvicorn - ASGI server

## Development

### Running Tests
```bash
# Backend (TODO)
pytest backend/tests/

# Frontend (TODO)
cd frontend && npm test
```

### Project Structure
See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed structure and design decisions.

## Documentation

- [QUICKSTART.md](./QUICKSTART.md) - 5-minute getting started guide
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed architecture and data flow
- [backend/README.md](./backend/README.md) - Backend API documentation
- [MIGRATION_SUMMARY.md](./MIGRATION_SUMMARY.md) - Repository reorganization notes

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Historical nutrition trends
- [ ] Personalized meal recommendations
- [ ] Integration with USDA/OpenFoodFacts databases
- [ ] Meal planning engine
- [ ] Recipe database
- [ ] Export functionality (PDF, CSV)
- [ ] Mobile app (React Native)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (when available)
5. Submit a pull request

## License

[Your License Here]

---

**Simple. Comprehensive. AI-Powered.**

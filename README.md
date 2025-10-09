# 🍽️ GoodFood - Nutrition Estimation from Descriptions

Simple AI-powered nutrition tracking. Just describe what you ate, agents estimate and verify the nutrients.

## 🏗️ How It Works

1. **Input Agent** estimates nutrients from meal description
2. **Critic Agent** verifies estimates (with OpenFoodFacts MCP if available)
3. Agents negotiate until consensus (80%+ approval)
4. Save to PostgreSQL with vector embeddings

**Input:** Natural language description
**Output:** 50+ nutrient values stored in database

## 🚀 Setup

```bash
# 1. Install
uv sync

# 2. Database (Docker)
docker run -d --name goodfood-postgres \
  -e POSTGRES_USER=goodfood_user \
  -e POSTGRES_PASSWORD=goodfood_pass \
  -e POSTGRES_DB=goodfood \
  -p 5432:5432 \
  ankane/pgvector

# 3. Configure
cp .env.example .env
# Edit .env - add ANTHROPIC_API_KEY and DATABASE_URL

# 4. Migrate
alembic upgrade head

# 5. Run
python main.py
```

## 📖 Usage

### Estimate from Description

```python
from src.workflows.estimation_workflow import EstimationWorkflow

workflow = EstimationWorkflow()

result = await workflow.run(
    description="Grilled chicken 200g with rice and broccoli"
)

# Result contains:
# - estimates: dict of all nutrients
# - iterations: number of rounds
# - approval: final approval %
```

### Save to Database

```python
from src.database.gateway import DatabaseGateway

db = DatabaseGateway()

record = await db.save_nutrition(
    name="Chicken with rice",
    description="Grilled chicken 200g with brown rice 150g...",
    meal_type=MealType.DINNER,
    nutrients=result["estimates"],
)
```

### Query History

```python
# Get recent meals
records = await db.get_history(limit=10)

# Search similar (TODO: implement vector search)
similar = await db.search_similar_by_description(embedding)
```

## 📊 Database Schema

```sql
CREATE TABLE nutrition_history (
    -- Identifiers
    id UUID,
    timestamp TIMESTAMPTZ,
    name VARCHAR(255),
    description VARCHAR(1000),
    meal_type VARCHAR(50),

    -- Embeddings for similarity search
    description_embedding vector(1536),
    nutrient_profile_embedding vector(1536),

    -- All nutrients as columns (50+)
    protein FLOAT,
    carbohydrates FLOAT,
    total_fats FLOAT,
    vitamin_c FLOAT,
    iron FLOAT,
    ...
);
```

## 🔧 Workflow Example

```
Description: "Grilled chicken 200g with rice and broccoli"

Iteration 1:
  → Estimator: protein=45g, carbs=50g, vitamin_c=80mg...
  → Critic: "Approval 75% - vitamin C seems high"

Iteration 2:
  → Estimator: (adjusts) vitamin_c=60mg...
  → Critic: "Approval 85% - looks good"

✅ Consensus reached!
💾 Saved to database
```

## 🗂️ Structure

```
goodfood/
├── src/
│   ├── agents/
│   │   ├── input_agent.py        # Estimates from description
│   │   └── input_critic.py       # Verifies estimates
│   ├── workflows/
│   │   └── estimation_workflow.py  # Negotiation loop
│   ├── database/
│   │   └── gateway.py            # CRUD + vector search
│   ├── models/
│   │   ├── nutrition.py          # 50+ nutrient fields
│   │   └── database.py           # SQLAlchemy schema
│   └── config/
│       ├── settings.py
│       └── nutrients.py
├── main.py                       # Example usage
└── alembic/versions/001_*.py     # DB schema
```

## ⚙️ Configuration

`.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://user:pass@localhost:5432/goodfood
MAX_ITERATIONS=5
APPROVAL_THRESHOLD=80
```

## 📝 Nutrients Tracked

50+ nutrients stored as individual columns:

- **Macros:** protein, carbohydrates, total_fats, fiber, water
- **Vitamins:** A, B1-B12, C, D, E, K
- **Minerals:** calcium, iron, zinc, magnesium, selenium
- **Amino Acids:** leucine, lysine, valine, isoleucine
- **Beneficial:** choline, taurine, coq10, beta_glucan
- **Phytonutrients:** beta_carotene, lycopene, quercetin

## 🔮 TODO

- [ ] Implement vector similarity search in `gateway.py`
- [ ] Generate description embeddings (OpenAI API)
- [ ] Generate nutrient profile embeddings (normalize values)
- [ ] Add OpenFoodFacts MCP integration for real data

## ✅ What Works

- ✅ Natural language input (just describe your meal)
- ✅ AI estimation with Claude
- ✅ Iterative verification workflow
- ✅ Database with all nutrient columns
- ✅ Vector embedding support (ready for similarity search)

---

**Simple. No complex JSON. Just describe and track.**

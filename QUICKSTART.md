# GoodFood Quick Start Guide

Get up and running with GoodFood in 5 minutes!

## Prerequisites

- Python 3.12+
- Node.js 18+
- Anthropic API key

## Step 1: Clone and Setup

```bash
# Clone repository
git clone <repo-url>
cd goodfood

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # or use uv
```

## Step 2: Configure Environment

Create `.env` file in repository root:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get your API key from: https://console.anthropic.com/

## Step 3: Start Backend

```bash
# From repository root
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

Backend is now running at `http://localhost:8000`

Test it: Open browser to `http://localhost:8000/health`

## Step 4: Start Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

You should see:
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

Frontend is now running at `http://localhost:5173`

## Step 5: Use the Application

1. Open browser to `http://localhost:5173`
2. You'll see the GoodFood homepage with:
   - Today's meals
   - Nutrient gaps
   - Next meal suggestion
3. Try adding a meal:
   - Type: "Grilled salmon with quinoa and broccoli"
   - Watch the real-time estimation process
   - See the meal added with full nutrition data

## How It Works

### Adding a Meal

1. **Enter description**: Type natural language description
2. **AI Estimation** (2-3 seconds):
   - Estimator analyzes ingredients
   - Verifier validates accuracy
   - Iterative refinement for precision
3. **Results**: Meal added with 70+ nutrients tracked

### Real-Time Updates

All connected clients see updates immediately:
- New meals appear instantly
- Nutrient gaps update
- Recommendations adjust

## Common Issues

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'anthropic'`

**Fix**: Install dependencies
```bash
pip install anthropic fastapi uvicorn
```

---

**Error**: `anthropic.AuthenticationError`

**Fix**: Check your `.env` file has correct API key

---

### Frontend won't connect

**Error**: WebSocket connection failed

**Fix**: Ensure backend is running on port 8000
```bash
curl http://localhost:8000/health
```

---

### Port already in use

**Backend (port 8000)**: Change port in `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Frontend (port 5173)**: Change in `vite.config.js`:
```javascript
server: { port: 5174 }
```

Update CORS in `backend/src/api/server.py` with new frontend port.

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture
- Read [backend/README.md](./backend/README.md) for backend details
- Explore the agent system in `backend/src/agents/`
- Check out the workflows in `backend/src/workflows/`

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- **Backend**: Automatically reloads when you edit Python files
- **Frontend**: Instantly updates when you edit React components

### Debugging

**Backend logs**: Watch the terminal running `backend/main.py`

**Frontend console**: Open browser DevTools (F12) → Console tab

**WebSocket traffic**: DevTools → Network tab → WS filter

### Testing Nutrition Estimation

Try these meal descriptions:
- "Oatmeal with berries and almond butter"
- "Chicken breast with sweet potato and green beans"
- "Greek yogurt with honey and walnuts"
- "Salmon sushi roll with edamame"
- "Quinoa bowl with chickpeas, avocado, and tahini"

Watch the real-time estimation process and see how the agents refine the estimates!

## Getting Help

- Check [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Check [backend/README.md](./backend/README.md) for API docs
- Review `backend/src/workflows/nutrition_workflow.py` for workflow details
- Inspect browser console for frontend errors
- Check backend terminal for server errors

## Docker Alternative

Want to run everything in containers?

```bash
docker-compose up
```

This starts:
- Backend on `http://localhost:8000`
- Frontend on `http://localhost:5173`
- PostgreSQL on `localhost:5432`

## What's Next?

You're now running GoodFood! Here's what you can explore:

1. **Track meals**: Add your actual meals and see nutrition estimates
2. **View components**: Check out the UI components in `frontend/src/components/`
3. **Customize agents**: Modify agent behavior in `backend/src/agents/`
4. **Add features**: Extend the system with new capabilities

Happy tracking! 🥗

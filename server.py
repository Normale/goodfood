"""FastAPI server with WebSocket streaming."""

import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from src.workflows.estimation_workflow import EstimationWorkflow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/estimate")
async def estimate_ws(websocket: WebSocket):
    """Stream estimation progress to client."""
    await websocket.accept()

    try:
        # Receive meal description
        data = await websocket.receive_json()
        description = data["description"]

        # Stream progress
        await websocket.send_json({"type": "start", "description": description})

        workflow = EstimationWorkflow()
        result = await workflow.run_streaming(description, websocket)

        await websocket.send_json({"type": "complete", "result": result})

    except Exception as e:
        await websocket.send_json({"type": "error", "error": str(e)})
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

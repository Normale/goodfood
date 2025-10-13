"""Main entry point for GoodFood backend server."""

import uvicorn

from backend.src.api.server import app

if __name__ == "__main__":
    uvicorn.run(
        "backend.src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files and README
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen

# Copy source code
COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "backend/main.py"]

FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir httpx==0.28.1 fastapi==0.119.1 uvicorn==0.38.0

# Copy agent code
COPY green_agent/main_http.py /app/main_http.py
COPY green_agent/agent_card.toml /app/agent_card.toml

# Copy experiments data (you'll need to have this available)
# COPY experiments /app/experiments

# Environment variables (can be overridden at runtime)
ENV PORT=8080
ENV AGENTBEATS_BACKEND_URL=https://agentbeats.org
ENV EXPERIMENTS_PATH=/app/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro

EXPOSE 8080

# Run the agent
CMD ["python", "main_http.py"]

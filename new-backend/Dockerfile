FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 MCP_DATA_DIR=/data

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . /app

# Ensure shared volume mountpoint exists (Compose will mount mcp_data here)
RUN mkdir -p /data
EXPOSE 8001

# Start FastAPI
# If your app is at app/main.py use app.main:app; if it's main.py at root, use main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

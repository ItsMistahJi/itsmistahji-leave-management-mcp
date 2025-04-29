FROM python:3.9-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN uv pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV DATA_DIR=/app/data

# Expose MCP server port
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]

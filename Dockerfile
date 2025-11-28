FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY examples/ ./examples/
COPY configs/ ./configs/

# Create non-root user
RUN useradd --create-home --shell /bin/bash agentic
USER agentic

# Expose port for API (future)
EXPOSE 8000

# Default command
CMD ["python", "-m", "agentic_framework.cli"]

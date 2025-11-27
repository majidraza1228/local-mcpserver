# Dockerfile for OpenShift deployment
FROM python:3.14-slim

LABEL maintainer="your-email@example.com" \
      description="MarkItDown MCP Server - HTTP Streaming API" \
      version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY markitdown_server/ ./markitdown_server/
COPY db_server/ ./db_server/

# Create necessary directories
RUN mkdir -p /tmp/uploads && \
    chmod 777 /tmp/uploads

# Create non-root user for security
RUN useradd -m -u 1001 -s /bin/bash appuser && \
    chown -R appuser:appuser /app /tmp/uploads

# Switch to non-root user
USER 1001

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Environment variables
ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Run server
CMD ["python", "-u", "markitdown_server/http_streaming_server.py"]

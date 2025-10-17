# Clone My Voice 2.0 - Optimized CPU-Only Dockerfile
# Based on NeuTTS-Air with improved efficiency

FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install only essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt ./

# Install Python dependencies with CPU-only PyTorch
# Explicitly use CPU-only index for smaller downloads
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask

# Final stage - minimal runtime image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install only runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY neuttsair /app/neuttsair
COPY web_interface /app/web_interface
COPY samples /app/samples
COPY requirements.txt /app/

# Create necessary directories with proper permissions
RUN mkdir -p /app/web_interface/uploads /app/web_interface/outputs && \
    chmod -R 755 /app/web_interface

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=web_interface/app.py \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
    CMD curl -f http://localhost:5000 || exit 1

# Run the application
CMD ["python", "-u", "web_interface/app.py"]

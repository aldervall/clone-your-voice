# Clone My Voice 2.0 - Refactored Architecture
# Optimized CPU-Only Dockerfile with clean code structure

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
    torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu && \
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

# Copy application code (new structure)
COPY src/ /app/src/
COPY templates/ /app/templates/
COPY main.py /app/
COPY requirements.txt /app/

# Create necessary directories with proper permissions
RUN mkdir -p /app/data/samples /app/data/uploads /app/data/outputs && \
    chmod -R 755 /app/data

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "-u", "main.py"]

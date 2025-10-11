FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including espeak
RUN apt-get update && apt-get install -y \
    espeak \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask && \
    pip install --no-cache-dir llama-cpp-python

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p /app/web_interface/uploads /app/web_interface/outputs

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=web_interface/app.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "web_interface/app.py"]

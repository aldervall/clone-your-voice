#!/bin/bash
# Clone My Voice 2.0 - Fast Build and Run Script

set -e

echo "================================================"
echo "Clone My Voice 2.0 - Speed Build"
echo "================================================"

# Stop any running containers
echo "→ Stopping existing containers..."
docker compose down 2>/dev/null || true

# Build with BuildKit (faster parallel builds)
echo "→ Building optimized image with BuildKit..."
DOCKER_BUILDKIT=1 docker compose build --no-cache

# Start the service
echo "→ Starting service..."
docker compose up -d

# Wait for healthcheck
echo "→ Waiting for service to be ready..."
for i in {1..30}; do
    if curl -sf http://localhost:5000 > /dev/null 2>&1; then
        echo "✓ Service is ready!"
        break
    fi
    echo "  Waiting... ($i/30)"
    sleep 2
done

# Show status
echo ""
echo "================================================"
echo "✓ Clone My Voice 2.0 is running!"
echo "================================================"
echo ""
echo "  Web Interface: http://localhost:5000"
echo ""
echo "  View logs:     docker compose logs -f"
echo "  Stop service:  docker compose down"
echo ""
docker compose ps
echo ""

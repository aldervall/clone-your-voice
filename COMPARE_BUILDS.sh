#!/bin/bash
# Compare original vs optimized Docker builds

echo "================================================"
echo "Docker Build Size Comparison"
echo "================================================"
echo ""

# Check if original image exists
ORIGINAL_SIZE=""
if docker images | grep -q "neutts-air-voice-cloning"; then
    ORIGINAL_SIZE=$(docker images neutts-air-voice-cloning:latest --format "{{.Size}}")
    echo "📦 Original (neutts-air):     $ORIGINAL_SIZE"
else
    echo "📦 Original (neutts-air):     Not built yet"
fi

# Check if new image exists
NEW_SIZE=""
if docker images | grep -q "clone-my-voice"; then
    NEW_SIZE=$(docker images clone-my-voice:2.0 --format "{{.Size}}")
    echo "📦 Optimized (v2.0):          $NEW_SIZE"
else
    echo "📦 Optimized (v2.0):          Not built yet"
    echo ""
    echo "Build it with: ./BUILD_AND_RUN.sh"
fi

echo ""
echo "================================================"
echo "Dockerfile Differences"
echo "================================================"
echo ""

# Show line count comparison
if [ -f ../neutts-air/Dockerfile.standard ]; then
    ORIG_LINES=$(wc -l < ../neutts-air/Dockerfile.standard)
    NEW_LINES=$(wc -l < Dockerfile)
    echo "Lines in original Dockerfile:  $ORIG_LINES"
    echo "Lines in optimized Dockerfile: $NEW_LINES"
    echo ""

    echo "Key differences:"
    echo "  ✓ Multi-stage build (builder + runtime)"
    echo "  ✓ Explicit CPU-only PyTorch index"
    echo "  ✓ Git removed from runtime"
    echo "  ✓ Better layer caching"
fi

echo ""
echo "================================================"
echo "Docker Compose Differences"
echo "================================================"
echo ""

if [ -f ../neutts-air/docker-compose.yml ]; then
    echo "Resource limits:"
    echo ""
    echo "Original:"
    grep -A 6 "deploy:" ../neutts-air/docker-compose.yml | head -7
    echo ""
    echo "Optimized (v2.0):"
    if grep -q "Resource limits removed" docker-compose.yml; then
        echo "  → Resource limits REMOVED for maximum speed!"
    else
        grep -A 6 "deploy:" docker-compose.yml | head -7
    fi
fi

echo ""
echo "================================================"
echo "Ready to test?"
echo "================================================"
echo ""
echo "  Build and run:  ./BUILD_AND_RUN.sh"
echo "  Manual build:   DOCKER_BUILDKIT=1 docker compose build"
echo "  Start service:  docker compose up -d"
echo ""

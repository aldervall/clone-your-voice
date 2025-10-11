#!/bin/bash

# NeuTTS-Air Docker Management Script

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  NeuTTS-Air Docker Management${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        echo "Please install Docker first: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
}

# Function to build the image
build() {
    echo -e "${BLUE}Building Docker image...${NC}"
    docker-compose build
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build successful${NC}"
    else
        echo -e "${RED}✗ Build failed${NC}"
        exit 1
    fi
}

# Function to start the container
start() {
    echo -e "${BLUE}Starting NeuTTS-Air container...${NC}"
    docker-compose up -d
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Container started successfully${NC}"
        echo ""
        echo -e "${GREEN}Access the web interface at:${NC}"
        echo -e "  ${YELLOW}http://localhost:5000${NC}"
        echo ""
        echo -e "To view logs: ${YELLOW}./docker-run.sh logs${NC}"
    else
        echo -e "${RED}✗ Failed to start container${NC}"
        exit 1
    fi
}

# Function to stop the container
stop() {
    echo -e "${BLUE}Stopping NeuTTS-Air container...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ Container stopped${NC}"
}

# Function to restart the container
restart() {
    echo -e "${BLUE}Restarting NeuTTS-Air container...${NC}"
    docker-compose restart
    echo -e "${GREEN}✓ Container restarted${NC}"
}

# Function to view logs
logs() {
    echo -e "${BLUE}Showing logs (Press Ctrl+C to exit)...${NC}"
    docker-compose logs -f
}

# Function to show status
status() {
    echo -e "${BLUE}Container status:${NC}"
    docker-compose ps
}

# Function to clean up
clean() {
    echo -e "${YELLOW}This will remove the container and image. Continue? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${BLUE}Cleaning up...${NC}"
        docker-compose down -v
        docker rmi neutts-air-neutts-air 2>/dev/null || true
        echo -e "${GREEN}✓ Cleanup complete${NC}"
    else
        echo -e "${YELLOW}Cleanup cancelled${NC}"
    fi
}

# Function to run bash in container
shell() {
    echo -e "${BLUE}Opening shell in container...${NC}"
    docker-compose exec neutts-air bash
}

# Main script
check_docker

case "${1:-}" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    shell)
        shell
        ;;
    "")
        # No argument - build and start
        build
        echo ""
        start
        ;;
    *)
        echo -e "${YELLOW}Usage: $0 {build|start|stop|restart|logs|status|clean|shell}${NC}"
        echo ""
        echo "Commands:"
        echo "  build    - Build the Docker image"
        echo "  start    - Start the container"
        echo "  stop     - Stop the container"
        echo "  restart  - Restart the container"
        echo "  logs     - View container logs"
        echo "  status   - Show container status"
        echo "  clean    - Remove container and image"
        echo "  shell    - Open bash shell in container"
        echo "  (no arg) - Build and start"
        exit 1
        ;;
esac

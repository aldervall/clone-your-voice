# NeuTTS-Air Docker Setup

Docker containerization for the NeuTTS-Air text-to-speech web interface.

## 🎯 Build Options

**Two build options available:**

1. **Full Build** (Recommended) - Includes llama-cpp-python for GGUF models
   - Build time: 5-10 minutes
   - Supports Q4/Q8 quantized models
   - Better performance

2. **Lite Build** - Faster, smaller, without llama-cpp-python
   - Build time: 2-3 minutes
   - Standard models only
   - Quick testing

📖 See [DOCKER_BUILD_OPTIONS.md](DOCKER_BUILD_OPTIONS.md) for detailed comparison.

## 🚀 Quick Start

### Option 1: Using the Management Script (Recommended)

```bash
# Full build (with llama-cpp-python)
./docker-run.sh

# Lite build (without llama-cpp-python, faster)
./docker-run.sh --lite

# Individual commands:
./docker-run.sh build     # Build the image
./docker-run.sh start     # Start the container
./docker-run.sh logs      # View logs
./docker-run.sh stop      # Stop the container
./docker-run.sh restart   # Restart the container
./docker-run.sh status    # Check status
./docker-run.sh shell     # Open shell in container
./docker-run.sh clean     # Remove container and image
```

### Option 2: Using Docker Compose Directly

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

## 🌐 Access

Once started, access the web interface at:
- **http://localhost:5000**

## 📁 Volume Mounts

The container uses these volume mounts:

- `./web_interface/uploads` - Uploaded reference audio files (persistent)
- `./web_interface/outputs` - Generated audio files (persistent)
- `./samples` - Sample voice files (read-only)

Generated audio and uploaded files are saved on your host machine and persist across container restarts.

## 🔧 Configuration

### Change Port

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Change 5000 to your preferred port
```

### Resource Limits

Add resource limits in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
    reservations:
      cpus: '1.0'
      memory: 2G
```

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
./docker-run.sh logs

# Check status
./docker-run.sh status
```

### Port already in use
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Or change the port in docker-compose.yml
```

### Model loading issues
The first run will download the AI models, which can take a few minutes. Check logs to see progress:
```bash
./docker-run.sh logs
```

### Permission issues with volumes
```bash
# Fix permissions for upload/output directories
sudo chown -R $USER:$USER web_interface/uploads web_interface/outputs
```

## 📊 Health Check

The container includes a health check that runs every 30 seconds:
```bash
# View health status
docker-compose ps
```

## 🧹 Cleanup

### Remove container only
```bash
docker-compose down
```

### Remove container and volumes
```bash
docker-compose down -v
```

### Full cleanup (container, image, volumes)
```bash
./docker-run.sh clean
```

## 🔄 Updates

To update to the latest code:
```bash
# Stop container
./docker-run.sh stop

# Pull latest code (if using git)
git pull

# Rebuild and restart
./docker-run.sh build
./docker-run.sh start
```

## 📋 System Requirements

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Disk Space**: ~5GB for image and models
- **RAM**: Minimum 2GB, recommended 4GB+
- **CPU**: Any modern CPU (GPU not required)

## 🎯 Production Deployment

For production use, consider:

1. **Use a reverse proxy** (nginx, Traefik, Caddy)
2. **Enable HTTPS**
3. **Set resource limits**
4. **Configure logging** (log rotation, centralized logging)
5. **Set up monitoring** (Prometheus, Grafana)
6. **Use environment variables** for sensitive config

Example nginx reverse proxy config:
```nginx
server {
    listen 80;
    server_name tts.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeout for model loading
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

## 🆘 Support

If you encounter issues:

1. Check logs: `./docker-run.sh logs`
2. Check status: `./docker-run.sh status`
3. Verify Docker installation: `docker --version && docker-compose --version`
4. Review GitHub issues: https://github.com/neuphonic/neutts-air/issues

## 📝 Notes

- The container runs on CPU by default (no GPU required)
- First run downloads models (~2GB), subsequent starts are faster
- Generated files persist on the host machine
- The container auto-restarts unless manually stopped

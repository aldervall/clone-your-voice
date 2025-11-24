# 🎙️ NeuTTS-Air Voice Cloning - Docker Deployment

> **Simple, browser-based voice cloning with Docker**

Clone your voice in 3 easy steps using AI-powered text-to-speech.

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 5GB disk space

### Deploy with Docker Compose

```bash
# 1. Clone the repository (or download the source)
cd neutts-air

# 2. Build and start the container
docker-compose up -d

# 3. Access the web interface
# Open http://localhost:5000 in your browser
```

That's it! The interface is ready to use.

## 📋 Features

✨ **Browser Recording** - Record your voice directly in the browser (10 seconds)
🎯 **Auto-Generated Prompts** - Read a random sentence for voice cloning
🎵 **Text-to-Speech** - Generate speech in your cloned voice
💾 **Download Audio** - Save your generated audio files
📱 **Mobile Friendly** - Works on phones, tablets, and desktops
🔄 **Persistent Storage** - Recordings and outputs are saved on the host

## 🎮 Usage

### Step 1: Record Your Voice
1. Open http://localhost:5000
2. Read the displayed prompt aloud
3. Click the microphone button (🎤)
4. Speak clearly for 10 seconds
5. Listen to the playback

### Step 2: Generate Speech
1. Click "Next: Generate Speech"
2. Type any text you want to hear
3. Click "Generate Speech"
4. Wait for processing (progress bar shows status)

### Step 3: Download
1. Listen to your synthesized speech
2. Click "Download Audio" to save
3. Or click "Generate Another" for more

## 🔧 Configuration

### Change Port

Edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Change 8080 to your preferred port
```

### Adjust Resources

Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'      # Max CPU cores
      memory: 4G       # Max RAM
    reservations:
      cpus: '2.0'      # Min CPU cores
      memory: 2G       # Min RAM
```

### Environment Variables

Available options:

```yaml
environment:
  - FLASK_ENV=production    # or 'development' for debug mode
  - BASE_URL=               # Optional: Base URL for frontend (e.g., https://yourdomain.com)
  - PYTHONUNBUFFERED=1      # Real-time logs
```

## 📁 Data Persistence

Data is stored in these directories:

```
./web_interface/uploads/    # User voice recordings
./web_interface/outputs/    # Generated audio files
./samples/                  # Demo voice samples (read-only)
```

All recordings and outputs persist on your host machine.

## 🛠️ Management Commands

### View Logs
```bash
docker-compose logs -f
```

### Restart Container
```bash
docker-compose restart
```

### Stop Container
```bash
docker-compose down
```

### Rebuild After Changes
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Check Status
```bash
docker-compose ps
```

### Access Container Shell
```bash
docker-compose exec neutts-air bash
```

## 🧹 Cleanup

### Remove Container Only
```bash
docker-compose down
```

### Remove Container + Volumes
```bash
docker-compose down -v
# WARNING: This deletes all recordings and outputs!
```

### Full Cleanup (Container + Image)
```bash
docker-compose down
docker rmi neutts-air-voice-cloning:latest
```

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Or change port in docker-compose.yml
```

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Check Docker status
docker ps -a
```

### Out of Memory
```bash
# Increase memory limit in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 8G  # Increase to 8GB
```

### Slow Performance
- Increase CPU allocation in `docker-compose.yml`
- Close other resource-intensive applications
- Ensure at least 4GB RAM available

### Permission Issues
```bash
# Fix upload/output directory permissions
sudo chown -R $USER:$USER web_interface/uploads web_interface/outputs
```

## 🏗️ Production Deployment

For production use, consider:

### 1. Use a Reverse Proxy (nginx)

```nginx
server {
    listen 80;
    server_name voice.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Increase timeout for model loading
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

### 2. Enable HTTPS (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d voice.yourdomain.com
```

### 3. Set Up Logging

Add to `docker-compose.yml`:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 4. Enable Monitoring

Use Docker stats:

```bash
# Real-time monitoring
docker stats neutts-air-web

# Or use Portainer for web UI
docker run -d -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce
```

## 📊 System Requirements

**Minimum:**
- 2 CPU cores
- 2GB RAM
- 5GB disk space

**Recommended:**
- 4 CPU cores
- 4GB RAM
- 10GB disk space

**Network:**
- No GPU required
- Works on CPU only
- Internet connection for first run (downloads AI models ~2GB)

## 🌐 Accessing from Other Devices

### Local Network Access

Change in `docker-compose.yml`:

```yaml
ports:
  - "0.0.0.0:5000:5000"  # Allow external connections
```

Then access from other devices:
```
http://<your-server-ip>:5000
```

### Firewall Configuration

```bash
# Allow port 5000 (UFW)
sudo ufw allow 5000/tcp

# Or (iptables)
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
```

## 📈 Performance Tips

1. **First Run**: Model download takes 2-5 minutes (one-time)
2. **Warm-up**: First generation is slower (~30-60s)
3. **Subsequent**: Later generations are faster (~10-20s)
4. **Recording Quality**: Use quiet environment, speak clearly
5. **Text Length**: Shorter texts (<500 words) process faster

## 🆘 Support

**Issues?**
1. Check logs: `docker-compose logs`
2. Verify requirements: `docker --version && docker-compose --version`
3. Restart container: `docker-compose restart`
4. GitHub Issues: https://github.com/neuphonic/neutts-air/issues

## 📝 Notes

- Container runs on CPU (no GPU needed)
- First run downloads AI models (~2GB)
- Models cache in container for faster restarts
- Generated files persist on host machine
- Auto-restart enabled (survives system reboots)

## 🎯 What's Next?

After deployment:
1. Try the demo voices (dave, jo, niklas)
2. Record your own voice
3. Generate custom speech
4. Share with your team!

---

**Built with ❤️ using NeuTTS-Air**
*AI-powered voice cloning made simple*

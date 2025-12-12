# Deployment Guide

This directory contains deployment configurations and scripts for the Vibe Hub Django application.

## Architecture

```
User → Cloudflare SSL → Cloudflare Tunnel → Nginx (Port 80)
                                      ↓
                           Static Files: Served directly by Nginx
                                      ↓
                           Django Requests: Proxied to Gunicorn (127.0.0.1:8000)
```

## Files Overview

- `nginx.conf` - Nginx configuration for serving static files and proxying Django
- `setup_nginx.sh` - Script to install and configure nginx
- `deploy_static.sh` - Script to collect and deploy static files
- `README.md` - This deployment guide

## Deployment Steps

### 1. Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-venv nginx

# Create application directory
sudo mkdir -p /opt/vibe-hub
sudo chown $USER:$USER /opt/vibe-hub
```

### 2. Application Setup

```bash
# Clone repository
cd /opt/vibe-hub
git clone <your-repo-url> .

# Create virtual environment
python3 -m venv vibe-hub-mvp

# Activate virtual environment
source vibe-hub-mvp/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create production environment file
cp .env.example .env
# Edit .env with production settings
```

### 3. Configure Nginx

```bash
# Run nginx setup script
sudo bash deployment/setup_nginx.sh

# The script will:
# - Install nginx if not present
# - Create directories for static files
# - Configure nginx with the provided config
# - Enable the site and reload nginx
```

### 4. Deploy Static Files

```bash
# Run static files deployment
bash deployment/deploy_static.sh

# This will:
# - Collect Django static files
# - Copy them to nginx directory (/var/www/static/)
# - Set proper permissions
```

### 5. Configure Systemd Service

```bash
# Copy systemd service file
sudo cp vibe-hub.service /etc/systemd/system/

# Create log directory
sudo mkdir -p /var/log/vibe-hub
sudo chown www-data:www-data /var/log/vibe-hub

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable vibe-hub
sudo systemctl start vibe-hub

# Check status
sudo systemctl status vibe-hub
```

### 6. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Generate sample data (optional)
python manage.py generate_sample_data
```

### 7. Configure Cloudflare Tunnel

Update your cloudflared configuration to point to nginx (port 80):

```yaml
# cloudflared config
ingress:
  - hostname: www.labyricorn.com
    service: http://10.138.0.121:80  # Point to nginx, not Django
  - service: http_status:404
```

## Production Environment Variables

Create `/opt/vibe-hub/.env` with:

```bash
# Core Settings
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=labyricorn.com,www.labyricorn.com,10.138.0.121,localhost,127.0.0.1

# Security Settings (with HTTPS via Cloudflare)
CSRF_COOKIE_SECURE=True
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
```

## Maintenance Commands

### Update Application
```bash
cd /opt/vibe-hub
git pull origin main
source vibe-hub-mvp/bin/activate
pip install -r requirements.txt
python manage.py migrate
bash deployment/deploy_static.sh
sudo systemctl restart vibe-hub
```

### View Logs
```bash
# Application logs
sudo journalctl -u vibe-hub -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Gunicorn logs
sudo tail -f /var/log/vibe-hub/access.log
sudo tail -f /var/log/vibe-hub/error.log
```

### Restart Services
```bash
# Restart Django application
sudo systemctl restart vibe-hub

# Restart nginx
sudo systemctl restart nginx

# Reload nginx configuration
sudo systemctl reload nginx
```

## Troubleshooting

### Static Files Not Loading
1. Check nginx configuration: `sudo nginx -t`
2. Verify static files exist: `ls -la /var/www/static/`
3. Check permissions: `ls -la /var/www/`
4. Redeploy static files: `bash deployment/deploy_static.sh`

### Application Not Starting
1. Check service status: `sudo systemctl status vibe-hub`
2. View logs: `sudo journalctl -u vibe-hub -n 50`
3. Test Gunicorn manually: `source vibe-hub-mvp/bin/activate && gunicorn --bind 127.0.0.1:8000 vibe_hub.wsgi:application`

### Nginx Issues
1. Test configuration: `sudo nginx -t`
2. Check if nginx is running: `sudo systemctl status nginx`
3. View error logs: `sudo tail -f /var/log/nginx/error.log`

## Security Notes

- Gunicorn binds to `127.0.0.1:8000` (localhost only) for security
- Nginx serves static files directly for performance
- All external traffic goes through nginx reverse proxy
- HTTPS is handled by Cloudflare tunnel
- Static files are cached for 1 year for performance
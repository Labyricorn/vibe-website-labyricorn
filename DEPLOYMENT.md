# Deployment Checklist

This document provides a step-by-step checklist for deploying the Labyricorn Vibe Hub application to production.

## Pre-Deployment Checklist

- [ ] All tests passing locally (`python manage.py test`)
- [ ] Code committed to version control
- [ ] Production server provisioned (Ubuntu LXC recommended)
- [ ] Domain name configured in Cloudflare
- [ ] Strong SECRET_KEY generated
- [ ] Database backup strategy planned

## Server Setup

### 1. System Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install python3 python3-pip python3-venv git -y

# Create application directory
sudo mkdir -p /opt/vibe-hub
sudo chown $USER:$USER /opt/vibe-hub
```

- [ ] System packages updated
- [ ] Python 3.10+ installed
- [ ] Git installed
- [ ] Application directory created

### 2. Application Setup

```bash
# Clone repository
cd /opt/vibe-hub
git clone <repository-url> .

# Create virtual environment
python3 -m venv vibe-hub-mvp

# Activate virtual environment
source vibe-hub-mvp/bin/activate

# Install dependencies
pip install -r requirements.txt
```

- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed

### 3. Environment Configuration

```bash
# Create .env file
cp .env.example .env
nano .env
```

Update `.env` with production values:

```env
SECRET_KEY=<generate-strong-random-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Security Settings
CSRF_COOKIE_SECURE=True
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
```

- [ ] `.env` file created
- [ ] SECRET_KEY generated and set
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] Security settings enabled

### 4. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

- [ ] Migrations applied
- [ ] Superuser created
- [ ] Static files collected

### 5. Gunicorn Service Setup

```bash
# Copy service file
sudo cp vibe-hub.service /etc/systemd/system/

# Create log directory
sudo mkdir -p /var/log/vibe-hub
sudo chown www-data:www-data /var/log/vibe-hub

# Set permissions
sudo chown -R www-data:www-data /opt/vibe-hub
sudo chmod -R 755 /opt/vibe-hub

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable vibe-hub
sudo systemctl start vibe-hub
sudo systemctl status vibe-hub
```

- [ ] Service file installed
- [ ] Log directory created
- [ ] Permissions set correctly
- [ ] Service enabled
- [ ] Service started successfully

### 6. Cloudflare Tunnel Setup

```bash
# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Authenticate
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create vibe-hub

# Note the tunnel ID
```

- [ ] cloudflared installed
- [ ] Authenticated with Cloudflare
- [ ] Tunnel created
- [ ] Tunnel ID recorded

### 7. Tunnel Configuration

```bash
# Create config directory
mkdir -p ~/.cloudflared

# Copy and edit config
cp cloudflared-config.example.yml ~/.cloudflared/config.yml
nano ~/.cloudflared/config.yml
```

Update with your tunnel ID and credentials path.

```bash
# Configure DNS
cloudflared tunnel route dns vibe-hub your-domain.com
cloudflared tunnel route dns vibe-hub www.your-domain.com

# Install as service
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
sudo systemctl status cloudflared
```

- [ ] Tunnel config created
- [ ] DNS records configured
- [ ] Tunnel service installed
- [ ] Tunnel service started

## Post-Deployment Verification

### 8. Testing

```bash
# Check Gunicorn service
sudo systemctl status vibe-hub

# Check Cloudflare tunnel
sudo systemctl status cloudflared

# View logs
sudo journalctl -u vibe-hub -n 50
sudo journalctl -u cloudflared -n 50
```

- [ ] Gunicorn service running
- [ ] Cloudflare tunnel running
- [ ] No errors in logs

### 9. Website Verification

Visit your domain and verify:

- [ ] Homepage loads correctly
- [ ] Static files (CSS/JS) loading
- [ ] Admin interface accessible at `/admin`
- [ ] Can log in to admin
- [ ] Can create and publish devlog
- [ ] Published devlog appears on homepage
- [ ] Devlog detail page works
- [ ] Project pages work
- [ ] RSS feed accessible at `/rss/`
- [ ] HTTPS working (via Cloudflare)

### 10. Security Verification

- [ ] Admin requires authentication
- [ ] HTTPS redirect working
- [ ] CSRF protection active
- [ ] XSS protection headers present
- [ ] No DEBUG information exposed
- [ ] Database file has correct permissions

## Backup Setup

### 11. Configure Automated Backups

```bash
# Create backup directory
mkdir -p /opt/vibe-hub/backups

# Add to crontab
crontab -e
```

Add this line:
```
0 2 * * * cp /opt/vibe-hub/db.sqlite3 /opt/vibe-hub/backups/db.sqlite3.$(date +\%Y\%m\%d)
```

- [ ] Backup directory created
- [ ] Automated backup scheduled
- [ ] Test backup manually

## Monitoring Setup

### 12. Log Monitoring

```bash
# Check log rotation
ls -la /var/log/vibe-hub/

# Set up log rotation (optional)
sudo nano /etc/logrotate.d/vibe-hub
```

Example logrotate config:
```
/var/log/vibe-hub/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload vibe-hub > /dev/null 2>&1 || true
    endscript
}
```

- [ ] Log rotation configured
- [ ] Monitoring strategy in place

## Maintenance Procedures

### Updating the Application

```bash
cd /opt/vibe-hub
source vibe-hub-mvp/bin/activate

# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart vibe-hub
```

### Rolling Back

```bash
cd /opt/vibe-hub

# Checkout previous version
git checkout <previous-commit-hash>

# Restore database backup if needed
cp /opt/vibe-hub/backups/db.sqlite3.YYYYMMDD /opt/vibe-hub/db.sqlite3

# Restart service
sudo systemctl restart vibe-hub
```

## Troubleshooting

### Common Issues

**Gunicorn won't start:**
```bash
sudo journalctl -u vibe-hub -n 50
# Check for Python errors, missing dependencies, or permission issues
```

**Static files not loading:**
```bash
python manage.py collectstatic --noinput --clear
sudo systemctl restart vibe-hub
```

**Database errors:**
```bash
# Check permissions
ls -la /opt/vibe-hub/db.sqlite3
sudo chown www-data:www-data /opt/vibe-hub/db.sqlite3
```

**Cloudflare tunnel not connecting:**
```bash
sudo journalctl -u cloudflared -n 50
cloudflared tunnel info vibe-hub
```

## Support Contacts

- **System Administrator**: [Your contact]
- **Cloudflare Support**: https://support.cloudflare.com/
- **Django Documentation**: https://docs.djangoproject.com/

## Deployment Complete!

Once all checklist items are complete, your Labyricorn Vibe Hub application should be live and accessible at your domain.

Remember to:
- Monitor logs regularly
- Keep dependencies updated
- Maintain regular backups
- Review security settings periodically

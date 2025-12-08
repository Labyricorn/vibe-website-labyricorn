# Deployment Files Reference

This document describes all deployment-related files in the project and their purposes.

## Configuration Files

### `.env.example`
**Purpose**: Template for environment variables  
**Location**: Project root  
**Usage**: Copy to `.env` and customize for your environment

Contains:
- Django configuration (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- Security settings for production
- Database configuration notes

### `requirements.txt`
**Purpose**: Python package dependencies  
**Location**: Project root  
**Usage**: `pip install -r requirements.txt`

Includes all required packages:
- Django 6.0
- Gunicorn (WSGI server)
- Hypothesis (property-based testing)
- Markdown (content processing)
- python-decouple (environment management)
- feedgen (RSS feeds)
- bleach (HTML sanitization)

## Service Configuration Files

### `vibe-hub.service`
**Purpose**: Systemd service configuration for Gunicorn  
**Location**: Project root (copy to `/etc/systemd/system/`)  
**Usage**: Manages Gunicorn as a system service

Configuration:
- Runs as `www-data` user
- Binds to `127.0.0.1:8000`
- 3 worker processes
- Automatic restart on failure
- Logs to `/var/log/vibe-hub/`

Installation:
```bash
sudo cp vibe-hub.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vibe-hub
sudo systemctl start vibe-hub
```

### `cloudflared-config.example.yml`
**Purpose**: Cloudflare Tunnel configuration template  
**Location**: Project root (copy to `~/.cloudflared/config.yml`)  
**Usage**: Routes traffic from Cloudflare to local Gunicorn

Configuration:
- Tunnel ID and credentials
- Ingress rules for domain routing
- Logging and connection settings

Installation:
```bash
cp cloudflared-config.example.yml ~/.cloudflared/config.yml
# Edit with your tunnel ID and domain
nano ~/.cloudflared/config.yml
```

## Documentation Files

### `README.md`
**Purpose**: Main project documentation  
**Location**: Project root  
**Audience**: Developers and administrators

Sections:
- Project overview and features
- Local development setup
- Testing instructions
- Content management guide
- Production deployment guide
- Troubleshooting
- Project structure
- Environment variables reference

### `DEPLOYMENT.md`
**Purpose**: Detailed deployment checklist  
**Location**: Project root  
**Audience**: System administrators

Sections:
- Pre-deployment checklist
- Step-by-step server setup
- Service configuration
- Post-deployment verification
- Backup setup
- Monitoring configuration
- Maintenance procedures
- Troubleshooting guide

### `DEPLOYMENT_FILES.md` (this file)
**Purpose**: Reference guide for deployment files  
**Location**: Project root  
**Audience**: Developers and administrators

## Deployment Scripts

### `deploy.sh`
**Purpose**: Automated deployment helper (Linux/macOS)  
**Location**: Project root  
**Usage**: `bash deploy.sh`

Features:
- Interactive menu for common tasks
- Run migrations
- Collect static files
- Run tests
- Create superuser
- Full deployment workflow
- Initial setup workflow

Make executable:
```bash
chmod +x deploy.sh
```

### `deploy.bat`
**Purpose**: Automated deployment helper (Windows)  
**Location**: Project root  
**Usage**: `deploy.bat`

Features:
- Same functionality as deploy.sh
- Windows-compatible batch script
- Interactive menu
- Error handling

## File Usage by Deployment Stage

### Initial Development Setup
1. `.env.example` → Copy to `.env`
2. `requirements.txt` → Install dependencies
3. `deploy.sh` or `deploy.bat` → Run initial setup

### Production Deployment
1. `requirements.txt` → Install on server
2. `.env.example` → Configure production `.env`
3. `vibe-hub.service` → Set up Gunicorn service
4. `cloudflared-config.example.yml` → Configure tunnel
5. `DEPLOYMENT.md` → Follow checklist

### Ongoing Maintenance
1. `deploy.sh` or `deploy.bat` → Run updates
2. `README.md` → Reference for procedures
3. `DEPLOYMENT.md` → Troubleshooting guide

## Quick Reference Commands

### Local Development
```bash
# Activate virtual environment
source vibe-hub-mvp/bin/activate  # Linux/macOS
vibe-hub-mvp\Scripts\activate     # Windows

# Run development server
python manage.py runserver

# Run tests
python manage.py test
```

### Production Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart vibe-hub
```

### Service Management
```bash
# Check service status
sudo systemctl status vibe-hub
sudo systemctl status cloudflared

# View logs
sudo journalctl -u vibe-hub -f
sudo journalctl -u cloudflared -f

# Restart services
sudo systemctl restart vibe-hub
sudo systemctl restart cloudflared
```

## Security Notes

### Files to Keep Secure
- `.env` - Contains SECRET_KEY and sensitive settings
- `db.sqlite3` - Contains all application data
- `~/.cloudflared/*.json` - Tunnel credentials

### Files to Commit to Git
- `.env.example` - Template only
- `requirements.txt` - Dependency list
- `vibe-hub.service` - Service template
- `cloudflared-config.example.yml` - Config template
- All documentation files
- Deployment scripts

### Files to Exclude from Git
- `.env` - Actual environment variables
- `db.sqlite3` - Database file
- `vibe-hub-mvp/` - Virtual environment
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files
- `logs/` - Log files

## Support and Updates

When updating deployment files:
1. Update the relevant file
2. Update this reference document
3. Update README.md if user-facing
4. Update DEPLOYMENT.md if affecting deployment process
5. Test changes in development environment
6. Document breaking changes clearly

## File Maintenance Schedule

- **Monthly**: Review security settings in `.env.example`
- **Quarterly**: Update `requirements.txt` dependencies
- **As Needed**: Update service configurations
- **With Each Release**: Update documentation

## Additional Resources

- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Gunicorn Documentation: https://docs.gunicorn.org/
- Cloudflare Tunnel Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- Systemd Service Guide: https://www.freedesktop.org/software/systemd/man/systemd.service.html

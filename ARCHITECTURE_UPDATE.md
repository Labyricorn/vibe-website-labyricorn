# Architecture Update: Nginx + Gunicorn Deployment

## Overview

The Vibe Hub application has been updated from a direct Gunicorn + Cloudflare Tunnel deployment to a more robust Nginx + Gunicorn + Cloudflare Tunnel architecture. This change resolves static file serving issues and improves performance and security.

## Architecture Changes

### Previous Architecture
```
User → Cloudflare SSL → Cloudflare Tunnel → Gunicorn (Port 8000)
                                      ↓
                           Static Files: Served by Django (inefficient)
```

### Current Architecture
```
User → Cloudflare SSL → Cloudflare Tunnel → Nginx (Port 80)
                                      ↓
                           Static Files: Served directly by Nginx
                                      ↓
                           Django Requests: Proxied to Gunicorn (127.0.0.1:8000)
```

## Key Benefits

1. **Performance**: Nginx serves static files directly, reducing Django load
2. **Security**: Gunicorn only accessible from localhost (127.0.0.1:8000)
3. **Caching**: Static files cached for 1 year with proper HTTP headers
4. **Reliability**: Nginx excels at serving static content and handling connections
5. **Scalability**: Better separation of concerns between static and dynamic content

## Configuration Changes

### Nginx Configuration
- **Location**: `deployment/nginx.conf`
- **Static Files**: Served from `/var/www/static/` with 1-year cache
- **Reverse Proxy**: Forwards dynamic requests to Gunicorn on 127.0.0.1:8000
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection

### Gunicorn Service
- **Binding**: Changed from `0.0.0.0:8000` to `127.0.0.1:8000` (localhost only)
- **Security**: No longer directly accessible from external network
- **Performance**: Focuses only on Django application logic

### Cloudflare Tunnel
- **Target**: Changed from port 8000 (Gunicorn) to port 80 (Nginx)
- **Configuration**: Updated `cloudflared-config.example.yml` to reflect new target

### Static File Deployment
- **Location**: Static files now deployed to `/var/www/static/`
- **Script**: `deployment/deploy_static.sh` handles collection and deployment
- **Permissions**: Proper ownership set to `www-data:www-data`

## New Deployment Scripts

### `deployment/setup_nginx.sh`
- Installs nginx if not present
- Creates static file directories
- Configures nginx site
- Sets proper permissions

### `deployment/deploy_static.sh`
- Collects Django static files
- Copies to nginx directory
- Sets proper permissions

## Updated Documentation

### Files Updated
- `README.md`: Updated deployment instructions and architecture diagrams
- `DEPLOYMENT.md`: Added nginx configuration steps and updated checklists
- `DEPLOYMENT_FILES.md`: Added nginx configuration file documentation
- `deployment/nginx.conf`: Updated server names to include production IP
- `cloudflared-config.example.yml`: Updated to point to port 80

### New Sections Added
- Nginx installation and configuration steps
- Static file deployment procedures
- Updated troubleshooting for nginx-specific issues
- Service management commands for nginx

## Migration from Previous Setup

If migrating from the old architecture:

1. **Install Nginx**: `sudo apt install nginx`
2. **Configure Nginx**: `sudo bash deployment/setup_nginx.sh`
3. **Deploy Static Files**: `bash deployment/deploy_static.sh`
4. **Update Cloudflare Tunnel**: Change target from port 8000 to port 80
5. **Restart Services**: Restart both nginx and gunicorn

## Maintenance Procedures

### Updating Static Files
```bash
# After code changes affecting static files
bash deployment/deploy_static.sh
```

### Service Management
```bash
# Check all services
sudo systemctl status nginx vibe-hub cloudflared

# Restart services
sudo systemctl restart nginx
sudo systemctl restart vibe-hub
```

### Log Monitoring
```bash
# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Application logs
sudo journalctl -u vibe-hub -f
sudo journalctl -u nginx -f
```

## Security Improvements

1. **Network Isolation**: Gunicorn no longer exposed to external network
2. **Static File Security**: Nginx handles static files with proper headers
3. **Request Filtering**: Nginx can filter malicious requests before reaching Django
4. **SSL Termination**: Handled by Cloudflare, with proper headers forwarded

## Performance Optimizations

1. **Static File Caching**: 1-year cache for static assets
2. **Compression**: Nginx can handle gzip compression
3. **Connection Handling**: Nginx efficiently manages client connections
4. **Resource Separation**: Django focuses on application logic only

## Troubleshooting

### Static Files Not Loading
1. Check nginx configuration: `sudo nginx -t`
2. Verify static files exist: `ls -la /var/www/static/`
3. Redeploy static files: `bash deployment/deploy_static.sh`
4. Check nginx error logs: `sudo tail -f /var/log/nginx/error.log`

### Service Issues
1. Check service status: `sudo systemctl status nginx vibe-hub`
2. Test nginx config: `sudo nginx -t`
3. Restart services in order: nginx, then vibe-hub

This architecture update provides a more robust, secure, and performant deployment suitable for production use.
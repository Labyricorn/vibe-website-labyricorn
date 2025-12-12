#!/bin/bash

# Nginx Setup Script for Vibe Hub
# This script configures nginx to serve static files and proxy Django requests

set -e  # Exit on any error

echo "Setting up Nginx for Vibe Hub..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install nginx if not already installed
if ! command -v nginx &> /dev/null; then
    echo "Installing nginx..."
    apt update
    apt install -y nginx
fi

# Create directories for static and media files
echo "Creating directories..."
mkdir -p /var/www/static
mkdir -p /var/www/media
chown -R www-data:www-data /var/www/

# Copy nginx configuration
echo "Configuring nginx..."
cp deployment/nginx.conf /etc/nginx/sites-available/vibe-hub
ln -sf /etc/nginx/sites-available/vibe-hub /etc/nginx/sites-enabled/

# Remove default nginx site
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

# Reload nginx
echo "Reloading nginx..."
systemctl reload nginx

# Enable nginx to start on boot
systemctl enable nginx

echo "Nginx setup complete!"
echo "Next steps:"
echo "1. Collect static files: python manage.py collectstatic --noinput"
echo "2. Copy static files: cp -r staticfiles/* /var/www/static/"
echo "3. Set permissions: chown -R www-data:www-data /var/www/"
echo "4. Start your Django app with Gunicorn on 127.0.0.1:8000"
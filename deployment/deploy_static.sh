#!/bin/bash

# Static Files Deployment Script
# Collects Django static files and copies them to nginx directory

set -e  # Exit on any error

echo "Deploying static files..."

# Activate virtual environment if it exists
if [ -d "vibe-hub-mvp" ]; then
    echo "Activating virtual environment..."
    source vibe-hub-mvp/bin/activate
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Copy to nginx directory (requires sudo)
echo "Copying static files to nginx directory..."
sudo cp -r staticfiles/* /var/www/static/

# Set proper permissions
echo "Setting permissions..."
sudo chown -R www-data:www-data /var/www/static/

echo "Static files deployed successfully!"
echo "Static files are now available at /var/www/static/"
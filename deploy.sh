#!/bin/bash
# Deployment script for Vibe Hub
# This script helps automate common deployment tasks

set -e  # Exit on error

echo "==================================="
echo "Vibe Hub Deployment Helper"
echo "==================================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please activate it first:"
    echo "  source vibe-hub-mvp/bin/activate"
    exit 1
fi

echo "✓ Virtual environment detected: $VIRTUAL_ENV"
echo ""

# Function to run migrations
run_migrations() {
    echo "Running database migrations..."
    python manage.py migrate
    echo "✓ Migrations complete"
    echo ""
}

# Function to collect static files
collect_static() {
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    echo "✓ Static files collected"
    echo ""
}

# Function to run tests
run_tests() {
    echo "Running test suite..."
    python manage.py test
    echo "✓ Tests passed"
    echo ""
}

# Function to create superuser
create_superuser() {
    echo "Creating superuser..."
    python manage.py createsuperuser
    echo "✓ Superuser created"
    echo ""
}

# Main menu
echo "Select deployment task:"
echo "1) Run migrations"
echo "2) Collect static files"
echo "3) Run tests"
echo "4) Create superuser"
echo "5) Full deployment (migrations + static + tests)"
echo "6) Initial setup (migrations + static + superuser)"
echo "7) Exit"
echo ""
read -p "Enter choice [1-7]: " choice

case $choice in
    1)
        run_migrations
        ;;
    2)
        collect_static
        ;;
    3)
        run_tests
        ;;
    4)
        create_superuser
        ;;
    5)
        echo "Running full deployment..."
        echo ""
        run_tests
        run_migrations
        collect_static
        echo "==================================="
        echo "✓ Full deployment complete!"
        echo "==================================="
        echo ""
        echo "Next steps:"
        echo "1. Restart Gunicorn: sudo systemctl restart vibe-hub"
        echo "2. Check logs: sudo journalctl -u vibe-hub -f"
        ;;
    6)
        echo "Running initial setup..."
        echo ""
        run_migrations
        collect_static
        create_superuser
        echo "==================================="
        echo "✓ Initial setup complete!"
        echo "==================================="
        echo ""
        echo "Next steps:"
        echo "1. Start development server: python manage.py runserver"
        echo "2. Or set up Gunicorn service for production"
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

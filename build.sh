#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Build frontend
cd frontend
npm ci
npm run build
cd ..

# Copy built frontend to Django static
mkdir -p journal/staticfiles/frontend
cp -r frontend/build/* journal/staticfiles/frontend/

# Change to Django project directory
cd journal

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser from env vars (only if set and user doesn't exist)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser --noinput || true
fi

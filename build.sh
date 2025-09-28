#!/bin/bash

# Clear pip cache
pip cache purge

# Install dependencies with no cache
pip install --no-cache-dir -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (if needed)
python manage.py migrate --noinput

echo "Build completed successfully!"

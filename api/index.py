import os
import sys
from django.core.wsgi import get_wsgi_application

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "solar_system_drf.settings")

# WSGI application
application = get_wsgi_application()

# Vercel expects this variable 👇
app = application

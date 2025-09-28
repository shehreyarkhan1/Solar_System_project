import os
import sys
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solar_system_drf.settings')

# Get the WSGI application
application = get_wsgi_application()

# For Vercel deployment
def handler(request):
    return application(request)

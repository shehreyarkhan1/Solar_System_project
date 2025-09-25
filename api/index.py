from django.core.wsgi import get_wsgi_application
import os

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solar_system_drf.settings')

# Get the WSGI application
application = get_wsgi_application()

# For Vercel deployment
def handler(request):
    return application(request)

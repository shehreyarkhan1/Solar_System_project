from solar_system_drf.wsgi import application
import os
from django.conf import settings
from django.http import HttpResponse
from django.views.static import serve

def handler(request):
    # Handle static files
    if request.path.startswith('/static/'):
        path = request.path[8:]  # Remove '/static/' prefix
        file_path = os.path.join(settings.STATIC_ROOT, path)
        if os.path.exists(file_path):
            return serve(request, path, document_root=settings.STATIC_ROOT)
    
    # Handle media files
    if request.path.startswith('/media/'):
        path = request.path[7:]  # Remove '/media/' prefix
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            return serve(request, path, document_root=settings.MEDIA_ROOT)
    
    # Handle all other requests with Django
    return application(request)

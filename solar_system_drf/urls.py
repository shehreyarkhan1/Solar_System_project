from django.contrib import admin
from django.urls import path, include
from myapp import views
from myapp.ADMIN.dashboard import Dashboard
from myapp.ADMIN.products import Products
from myapp.ADMIN import registeruser
from myapp.ADMIN.registeruser import deleteuser
from myapp.ADMIN import home
from myapp.ADMIN import login
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  # Fixed typo

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    # ADMIN URLS
    # Login URL
    path("login/", login.loginuser, name="login"),
    path("logout/", login.logoutuser, name="logout"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("products/", Products.as_view(), name="products"),
    path("products/update/", Products.as_view(), name="productsupdate"),
    # Slider management URLs - FIXED
    path("slider/", home.homepage, name="homepage"),
    # users
    path("registeruser/", registeruser.registeruser, name="registeruser"),
    path(
        "deleteuser/<int:id>/", deleteuser, name="deleteuser"
    ),  # ✅ now it’s a function
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

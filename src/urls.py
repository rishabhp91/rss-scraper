# Python module
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Third party module
from rest_framework.authtoken import views as authviews
from rest_framework.schemas import get_schema_view

# For API versioning
APP_VERSION_PREFIX = "v1/"

# Url routes for this project
urlpatterns = [
    # For Django Admin portal
    path("admin/", admin.site.urls),
    # RSS App Urls - with versioning
    path(APP_VERSION_PREFIX, include("src.rss.urls")),
    # Authentication
    path(
        "login",
        authviews.obtain_auth_token,
        name="login",
    ),
    # API Documentation
    path(
        "openapi",
        get_schema_view(
            title="RSS Scraper", description="API for RSS Management", version="1.0.0"
        ),
        name="openapi-schema",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

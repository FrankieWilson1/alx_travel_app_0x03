from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Api metadata for Swagger documentation
# Matches 'DEFAULT_INFO': 'alx_travel_app.urls.api_info' in settings.py
api_info = openapi.Info(
    title="ALX Travel App API",
    default_version='v1',
    description="API documentation for the ALX Travel Listing Platform",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@frankuwill101@gmail.com"),
    license=openapi.License(name=""),
)

# Get Schema view for swagger and Redoc
schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs for 'listing' app
    path('api/', include('listings.urls')),
    # DRF browsable API loging/logout views
    path('api-auth/', include('rest_framework.urls')),

    # Swagger API Documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

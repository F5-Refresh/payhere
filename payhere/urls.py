"""payhere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_url_patterns = [path('users', include('users.urls')), path('', include('account_books.urls'))]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title='payhere',
        default_version='v1',
        description="payhere API",
    ),
    public=True,
    permission_classes=[AllowAny],
    patterns=schema_url_patterns,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', include('users.urls')),
    path('', include('account_books.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import VerifiedTokenObtainPairView

def health(request):
    return JsonResponse({"ok": True})

urlpatterns = [
    path("admin/", admin.site.urls),

    # health for docker-compose healthcheck
    path("health/", health),

    # JWT
    path("token/", VerifiedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # apps
    path("accounts/", include("accounts.urls")),
    path("internships/", include("internships.urls")),
]
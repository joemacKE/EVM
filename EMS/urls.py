
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('events.api.urls')),
    path('api/', include('accounts.api.urls')),

    # JWT Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    
]

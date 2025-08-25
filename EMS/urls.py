
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
    # path('api/accounts/', include('accounts/api.urls')),
    path('api/events/', include('events.api.urls')),
    path('api/users/', include('accounts.api.urls')),

    # JWT Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh-view'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),

]

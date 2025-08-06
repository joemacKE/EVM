from django.urls import path, include
from events.api.views import  EventViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')


urlpatterns = [
    path('api/', include(router.urls)),
    # path('list/', EventListAPIView.as_view(), name='event-list'),
    # path('<int:pk>/', EventDetailAPIView.as_view(), name='event-details'),
]
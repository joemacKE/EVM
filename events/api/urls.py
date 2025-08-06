from django.urls import path, include
from events.api.views import EventListAPIView, EventDetailAPIView, EventViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')


urlpatterns = [
    path('list/', EventListAPIView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailAPIView.as_view(), name='event-details'),
]
from django.urls import path, include
from events.api.views import EventListAPIView, EventDetailAPIView




urlpatterns = [
    # path('api/', include(router.urls)),
    path('list/', EventListAPIView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailAPIView.as_view(), name='event-details'),
]
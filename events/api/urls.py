from django.urls import path, include
from events.api.views import event_list, event_details

urlpatterns = [
    path('list/', event_list, name='event-list'),
    path('<int:pk>/', event_details, name='event-details'),
]
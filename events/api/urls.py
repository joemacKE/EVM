from django.urls import path, include
from events.api.views import EventListAPIView, EventDetailAPIView, CommentListAPIView, CommentDetailAPIView




urlpatterns = [
    # path('api/', include(router.urls)),
    path('list/', EventListAPIView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailAPIView.as_view(), name='event-details'),
    path('<int:event_id>/comments/', CommentDetailAPIView.as_view(), name='add-post-comments'),
    path('<int:event_id>/comments/', CommentListAPIView.as_view(), name = 'comment-list'),
]
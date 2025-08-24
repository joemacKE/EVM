from django.urls import path, include
from events.api.views import (
    EventListAPIView,
    EventFilterList,
    EventDetailAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    LikePostAPIView,
    UnlikePostAPIView,
    )




urlpatterns = [
    # path('api/', include(router.urls)),
    path('list/', EventListAPIView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailAPIView.as_view(), name='event-details'),
    path('<int:event_id>/comments/', CommentDetailAPIView.as_view(), name='add-post-comments'),
    path('<int:event_id>/comments/', CommentListAPIView.as_view(), name = 'comment-list'),
    path('<int:pk>/like/', LikePostAPIView.as_view(), name='like'),
    path('<int:event_id>/unlike/', UnlikePostAPIView.as_view(), name='unlike'),
    path('filter/', EventFilterList.as_view(), name='event-list'),
]
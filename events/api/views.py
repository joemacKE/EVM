from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.authentication import (SessionAuthentication, BasicAuthentication, TokenAuthentication)
from events.api.serializers import EventSerializer, CommentSerializer, BookSerializer
from rest_framework.response import Response
from events.models import Event, Comment, Like
from notifications.models import Notification
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class EventFilterList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'organizer', 'location', 'start_date', 'start_time']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination 

class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = ['status']

class EventListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        # retrieves all events
        try:

            queryset = Event.objects.all()
            filterset = EventFilter(request.GET, queryset=queryset)
        except Event.DoesNotExist:
            return Response({'error': 'No events found'}, status=status.HTTP_404_NOT_FOUND)
        if filterset.is_valid():
            queryset = filterset.qs
        
        # Serialize the events
        if not queryset:
            return Response({'message': 'No events available'}, status=status.HTTP_200_OK)
        
        
        # Return the serialized data
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = EventSerializer(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)  # Set organizer here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #retrieves a single event by ID
    def get(self, request, pk):

        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def post(self, request, pk):
        #creating and posting an event
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request, pk):
        #retreiving and updating a singl event by an ID
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event Not Found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        #deleting a single event by ID
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response("Event is deleted succesfully", status = status.HTTP_200_OK)

class CommentListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'No event by that ID found'}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(event_id = event_id) 
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class CommentDetailAPIView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, event_id):
#         try:
#             event = Event.objects.get(pk=event_id)
#         except Event.DoesNotExist:
#             return Response({'error': 'No event by that ID found'}, status=status.HTTP_404_NOT_FOUND)
#         comments = Comment.objects.filter(event_id = event_id) 
#         serializer = CommentSerializer(data=request.data,  many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentDetailAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event, author=request.user)  # inject automatically
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    

class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def post(self, request, pk):
        event = generics.get_object_or_404(Event, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, event=event)

        if not created:
            # User already liked → Unlike instead
            like.delete()
            return Response({'message': 'Event unliked successfully!'}, status=status.HTTP_200_OK)

        # If user newly liked, send notification
        if event.organizer != request.user:
            Notification.objects.create(
                recipient=event.organizer,
                actor=request.user,
                verb='liked your event',
                target=event
            )

        return Response({'message': 'Event liked successfully!'}, status=status.HTTP_201_CREATED)


class UnlikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

    def post(self, request, event_id):
        try:
            event = generics.get_object_or_404(Event, pk=event_id)
        except Event.DoesNotExist:
            return Response({'error':'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        like = Like.objects.filter(user=request.user, event =event).first()

        if not like:
            return Response({'error': 'You have not liked this event yet'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'message': 'Like deleted succesfully'})

class BookEventView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, SessionAuthentication]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event cannot be found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(user=request.user, event=event)
            event.attendees.add(request.user)
            return Response(BookSerializer(booking).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





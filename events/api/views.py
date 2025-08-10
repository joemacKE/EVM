from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import (SessionAuthentication, BasicAuthentication)
from events.api.serializers import EventSerializer
from rest_framework.response import Response
from events.models import Event
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from django.utils import timezone

# import django_filters.rest_framework 


class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user

class EventListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # retrieves all events
        try:
            events = Event.objects.all()
        except Event.DoesNotExist:
            return Response({'error': 'No events found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the events
        if not events:
            return Response({'message': 'No events available'}, status=status.HTTP_200_OK)
        
        # Return the serialized data
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)  # Set organizer here!
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
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




# @api_view(['GET', 'POST'])
# def event_list(request):
#     if request.method == "GET":
#         try:
#             event = Event.objects.all()
#         except Event.DoesNotExist:
#             return Response({'error': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = EventSerializer(event, many=True)
#         return Response(serializer.data)
    
#     if request.method == "POST":
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])       
# def event_details(request, pk):
#     if request.method == "GET":
#         try:
#             event = Event.objects.get(pk=pk)
#         except Event.DoesNotExist:
#             return Response({'error': 'Event Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = EventSerializer(event)
#         return Response(serializer.data)
    
#     if request.method == "PUT":
#         try:
#             event = Event.objects.get(pk=pk)
#         except Event.DoesNotExist:
#             return Response({'error': 'Event Not Found'}, status = status.HTTP_404_NOT_FOUND)
#         serializer = EventSerializer(event, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
    
#     if request.method == "DELETE":
#         try:
#             event = Event.objects.get(pk=pk)
#         except Event.DoesNotExist:
#             return Response({"error": "Event Not Found"}, status=status.HTTP_404_NOT_FOUND)
#         event.delete()
#         return Response("Event is deleted succesfully", status = status.HTTP_200_OK)



# class EventFilter(django_filters.FilterSet):
#     organizer = django_filters.CharFilter(field_name="organizer", lookup_expr="icontains")
#     category = django_filters.CharFilter(field_name="category", lookup_expr="exact")
#     status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    
#     class Meta:
#         model = Event
#         fields = ['organizer', 'category', 'status']

# class EventViewSet(viewsets.ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
#     filterset_class = EventFilter

#     def perform_create(self, serializer):
#         serializer.save(organizer =self.request.user)
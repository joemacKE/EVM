from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from events.api.serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.models import Event
from rest_framework import status, viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters import filters

class EventFilter(filters.FilterSet):

    class Meta:
        model = Event
        fields = {
            'organizer': ['icontains'],
            "category": ['upcoming', 'ongoing', 'cancelled', 'completed'],
            'status': ['conference', 'webinar', 'meet_and_greet', 'hackathon', 'coding_bootcamp', 'movie_night', 'RnB Night',
                       'Pack and Chill', 'Pack and Grill']
        }

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter



class EventListAPIView(APIView):
    #retrieving list of events listed
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class EventDetailAPIView(APIView):
    #class EventDetailMixin(LoginRequiredMixin, View):
        #login_url = "accounts/api/login"
        #redirect_name = "redirect_to"

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
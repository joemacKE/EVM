from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from events.api.serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.models import Event
from rest_framework import status

class EventListAPIView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class EventDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event Not Found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
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
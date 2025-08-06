from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

class RegisterView(APIView):
    # def get(self, request, pk):
    #     user = 
    #     serializer = RegisterSerializer(data=request.data)


    def post(self, request):
        #registering a user
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User is registered succesfully"}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        
        #updating user profile
        ...

    def delet(self, request):
        #deleting an account
        ...
    
class LogOutView(APIView):
    ...
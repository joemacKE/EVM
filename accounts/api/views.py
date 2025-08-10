from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #logging out a user and blacklisting the token
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "You have been logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
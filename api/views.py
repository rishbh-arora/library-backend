# views.py
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer

class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=201)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)
    

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'status_code': 200,
                    'status': "success",
                    'username': user.username,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {
                    'status_code': 400,
                    'status': "error",
                    'errors': e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        return serializer.save()

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        print(username,email,password)  
    
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'status_code':200,
                        'status':"success",
                        'username': user.username,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    })
        elif email and password:
            queryset = User.objects.filter(email=email).first()
            if queryset:
                user = authenticate(username=queryset.username,password=password)
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'status_code':200,
                        'status':"success",
                        'email': user.email,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    })
                
                else:
                    return Response({
                        'status_code':403,
                        'status':"error",
                        'message': "User account is disabled"
                    })
            else:
                return Response({
                        'status_code':403,
                        'status':"error",
                        'message': "Unable to log in with provided credentials."
                    })
        else:
            return Response({
                        'status_code':403,
                        'status':"error",
                        'message': 'Must include "username" and "password'
                    })
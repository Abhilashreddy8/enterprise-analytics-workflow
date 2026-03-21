from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer


from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminUserRole


class AdminOnlyView(APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        return Response({
            "message": "Only admin can see this"
        })
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "This is protected data",
            "user": request.user.email
        })
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from .serializers import *


class PublicUserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=SignupSerializer,
    )
    def signup(self, request):
        """
        {
            "email": "email",
            "password": "password",
            "confirm_password":"confirm_password",
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=SendVerificationCodeSerializer,
        permission_classes=(AllowAny,),
    )
    def send_verification_code(self, request):
        """
        {
            "email": "email",
            "reason": "code_reason",
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.send_code()
            return Response(
                {"message": "Successfully send OTP!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=VerifyCodeSerializer,
        permission_classes=(AllowAny,),
    )
    def verify_code(self, request):
        """
        {
            "email": email,
            "code": code,
        }
        """
        serializer = self.serializer_class(
            data=request.data,
            context={"user_checking": True},
        )
        if serializer.is_valid():
            serializer.verify_code()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=SigninSerializer,
    )
    def signin(self, request):
        """
        {
            "username": username,
            "password": password
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user, token = serializer.signin()
            data = UserSerializer(user).data
            data["token"] = token
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

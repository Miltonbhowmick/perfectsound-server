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

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=ForgetPasswordSerializer,
    )
    def forget_password(self, request):
        """
        {
            "email": email,
            "code": code,
            "password": new-password
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.forget_password()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(IsAuthenticated,),
        serializer_class=ChangePasswordSerializer,
    )
    def change_password(self, request):
        """
        {
            "old_password": old_password,
            "new_password": new_password,
            "new_password2": new_password2
        }
        """
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            user = serializer.change_password()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get", "patch", "delete"],
        serializer_class=UserSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def profile(self, request, pk=None):
        """
        {
            "nickname": "",
            "email": "",
            "gender": 0,1,2
            "birth_year": year,
        }
        """
        user = request.user

        if self.request.method == "GET":
            data = self.serializer_class(user).data
            return Response(data, status=status.HTTP_200_OK)
        elif self.request.method == "PATCH":
            serializer = self.serializer_class(
                instance=user, data=request.data, partial=True
            )
            if serializer.is_valid():
                user_obj = serializer.save()
                data = UserSerializer(user_obj).data
                return Response(data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif self.request.method == "DELETE":
            obj = user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(IsAuthenticated,),
        serializer_class=VerifyPasswordSerializer,
    )
    def verification(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={"user": user})
        if serializer.is_valid():
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=NewsletterCreateSerializer,
    )
    def newsletter(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            newsletter = serializer.save()
            newsletter.send_newsletter()
            return Response(
                NewsletterSerializer(newsletter).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

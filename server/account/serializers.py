from rest_framework import serializers
import re

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    def validate_password(self, value):
        """
        Validate that the password contains at least one uppercase letter, one number,
        and one special character from the specified set.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        if not re.search(r"[~!@#$%^&*]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character (~!@#$%^&*)."
            )
        return value

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return data

    # def create(self, validated_data):
    #     email = validated_data.get("email")
    #     password = validated_data.pop("password", None)

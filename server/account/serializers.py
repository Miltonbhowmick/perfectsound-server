from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.utils import timezone
import re
import random
from .models import *
from .auth_backend import UsernameOrEmailModelBackend


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "user_permissions", "groups")


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
    code = serializers.IntegerField(required=False)

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
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["Email is already exists."]})
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.pop("password", None)
        code = validated_data.get("code", None)
        username = email.split("@")[0] + str(random.randint(0, 3))
        user = User(username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    reason = serializers.CharField(required=False)

    def validate(self, validated_data):
        email = validated_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["Email is not found!"]})
        return validated_data

    def send_code(self):
        email = self.validated_data.get("email")
        reason = self.validated_data.get("reason", None)

        User.send_verification_code(User, reason=reason, email=email)
        return None


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True)

    def validate(self, validated_data):
        email = validated_data.get("email")
        code = validated_data.get("code")

        try:
            verification_obj = Verification.objects.get(email=email)
        except:
            verification_obj = None

        if verification_obj is None:
            raise serializers.ValidationError({"email": ["Not found!"]})
        else:
            if verification_obj.code != code:
                raise serializers.ValidationError({"code": ["Invalid code!"]})
        return validated_data

    def verify_code(self):
        email = self.validated_data.get("email")
        code = self.validated_data.get("code")
        user_checking = self.context.get("user_checking", True)

        verification_obj = Verification.objects.get(email=email, code=code)
        verification_obj.code = None
        verification_obj.save()

        if user_checking == True:
            user = User.objects.get(email=email)
            user.is_email_verified = True
            user.save()
            # send email verification
        return True


class SigninSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )

    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = UsernameOrEmailModelBackend.authenticate(
            self, username=email, password=password
        )
        if not user:
            raise serializers.ValidationError({"email": ["Incorrect Username/Email!"]})
        else:
            if not user.is_active:
                raise serializers.ValidationError(
                    {"email": ["Account is blocked! Please contact support!"]}
                )
        return validated_data

    def signin(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        user = UsernameOrEmailModelBackend.authenticate(
            self, username=email, password=password
        )

        if user.is_email_verified and user.is_2fa == False:
            token, token_created = Token.objects.get_or_create(user=user)
            token = token.key
        else:
            token = None

        user.last_login = timezone.now()
        user.save()

        return user, token


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True)
    password = serializers.CharField(style={"input_type": "password"})

    def validate_password(self, value):
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

    def validate(self, validated_data):
        email = validated_data.get("email")
        code = validated_data.get("code")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["Email not found!"]})

        try:
            verification_obj = Verification.objects.get(email=email)
        except:
            verification_obj = None

        if verification_obj is None:
            raise serializers.ValidationError({"email": ["Not found!"]})
        else:
            if verification_obj.code != code:
                raise serializers.ValidationError({"code": ["Invalid code!"]})

        return validated_data

    def forget_password(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        verification_obj = Verification.objects.get(email=email)
        verification_obj.code = None
        verification_obj.save()
        return None


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(style={"input_type": "password"})
    new_password2 = serializers.CharField(style={"input_type": "password"})

    def validate_old_password(self, value):
        user = self.context["user"]
        if not user.check_password(value):
            raise serializers.ValidationError("Old password entered incorrectly!")
        return value

    def validate_new_password(self, value):
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

    def validate_new_password2(self, value):
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

    def validate(self, validated_data):
        new_password = validated_data.get("new_password")
        new_password2 = validated_data.get("new_password2")

        if new_password != new_password2:
            raise serializers.ValidationError(
                {"new_password": ["The 2 password field not matched!"]}
            )
        return validated_data

    def change_password(self):
        password = self.validated_data.get("new_password")
        user = self.context["user"]
        user.set_password(password)
        user.save()
        return user

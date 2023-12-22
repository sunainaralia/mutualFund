from rest_framework import serializers
import random
from .models import (
    User,
    UserBasicDetail,
    PanVerification,
    AdharCardVerify,
    UserPurchaseOrderDetails,
)
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.authentication import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

from api.v1.mutual_sip.models import SIP


# serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "phone_no",
            "referral_code",
            "profile_photo",
            "is_blocked",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


# serializer for login
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


# serializer for change password
class UserChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(style={"input_type": "password"})
    password2 = serializers.CharField(style={"input_type": "password"})
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["password1", "password2", "password"]


# serializer for send password reset email
# class SendResetPasswordEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255)

#     class Meta:
#         fields = ["email"]

#     def validate(self, attrs):
#         email = attrs.get("email")
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             link = "http://localhost:3000/api/user/reset/" + uid + "/" + token
#             body = "click following link to reset your password" + link
#             print(body)
#             data = {
#                 "subject": "Reset your password",
#                 "body": body,
#                 "to_email": user.email,
#             }
#             Util.send_email(data)
#             return attrs
#         else:
#             raise serializers.ValidationError("this email is not registered")


class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp = random.randrange(100000, 1000000)
            link = str(otp)
            body = "Your Otp is:" + link
            data = {
                "subject": "Reset your password",
                "body": body,
                "to_email": user.email,
                "otp": otp,
                "id": user.id,
            }
            Util.send_email(data)
            return data
        else:
            raise serializers.ValidationError("This email is not registered")


# password reset serializer
class UserResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    otp = serializers.CharField()

    class Meta:
        fields = ["password1", "password2", "otp"]

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        otp = attrs.get("otp")
        id = self.context.get("id")
        validate_otp = self.context.get("otp")
        if otp == validate_otp:
            user = User.objects.get(id=id)
            if password1 != password2:
                raise serializers.ValidationError(
                    "password and confirm password are not matched"
                )
            user.set_password(password1)
            user.save()
            return attrs
        else:
            raise serializers.ValidationError("invalid otp")


# serializer for user profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone_no",
            "referral_code",
            "profile_photo",
        ]


# serializer for basic details
class UserBasicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBasicDetail
        fields = [
            "id",
            "nationality",
            "fullName",
            "d_o_b",
            "address_details",
            "zip_code",
            "state",
            "user",
            "verification",
        ]


# serializer for pan verification
class UserPanVerification(serializers.ModelSerializer):
    class Meta:
        model = PanVerification
        fields = ["id", "pan_card", "pan_no"]


# serializer for adhar verification
class UserAdharVerification(serializers.ModelSerializer):
    class Meta:
        model = AdharCardVerify
        fields = ["id", "adhar_card_front", "adhar_no", "adhar_card_back"]


class SipSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIP
        fields = [
            "id",
            "name",
            "current_annual_return_rate",
            "min_amount",
            "current_value",
            "time_period",
            "created_at",
            "no_of_investors",
            "total_investment",
            "investment_type",
            "sip_status",
            "gain_value",
            "sip_photo",
        ]


class UserPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPurchaseOrderDetails
        fields = [
            "id",
            "sips",
            "invested_amount",
            "member_status",
            "user",
            "portfolio_no",
            "sip_price",
            "invested_period",
            "installment_date",
            "no_of_installment",
            "sip_type",
            "investment_type",
            "date_of_purchase",
        ]

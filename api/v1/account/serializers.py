from rest_framework import serializers
import random
from .models import (
    User,
    UserBasicDetail,
    PanVerification,
    AdharCardVerify,
    UserPurchaseOrderDetails,
    PreviousCurrentValueLog,
)
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.authentication import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from django.db import models
from api.v1.mutual_sip.models import SIP


# serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "phone_no",
            "referral_code",
            "profile_photo",
            "is_blocked",
            "verification",
            "created_at",
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
            "verification",
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
            "city",
        ]


# serializer for pan verification
class UserPanVerification(serializers.ModelSerializer):
    class Meta:
        model = PanVerification
        fields = ["id", "pan_card", "pan_no", "user"]

    def validate(self, attrs):
        pan_no = attrs.get("pan_no")
        if len(pan_no) == 10:
            return attrs
        else:
            raise serializers.ValidationError("pan card no. must be 10 digit no")


# serializer for adhar verification
class UserAdharVerification(serializers.ModelSerializer):
    class Meta:
        model = AdharCardVerify
        fields = ["id", "adhar_card_front", "adhar_no", "adhar_card_back"]

    def validate(self, attrs):
        adhar_no = attrs.get("adhar_no")
        if len(adhar_no) == 10:
            return attrs
        else:
            raise serializers.ValidationError("adhar card no. must be 10 digit no")


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


class PreviousCurrentValueLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousCurrentValueLog
        fields = ["current_value", "timestamp"]


class UserPurchaseOrderSerializer(serializers.ModelSerializer):
    logs = PreviousCurrentValueLogSerializer(many=True, read_only=True)

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
            "current_value",
            "logs",
            "payment_type",
        ]


# userallbasicdetails


class UserDetailsSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    invested_amount = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    member_status = serializers.SerializerMethodField()
    current_value=serializers.SerializerMethodField()
    kyc_status = serializers.SerializerMethodField()
    portfolio_no=serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "profile_photo",
            "username",
            "email",
            "created_at",
            "state",
            "is_blocked",
            "invested_amount",
            "city",
            "member_status",
            "phone_no",
            "current_value",
            "kyc_status",
            "portfolio_no",
        ]

    def get_state(self, obj):
        user_basic_detail = obj.userbasicdetail.first()
        return user_basic_detail.state if user_basic_detail else None

    def get_city(self, obj):
        user_basic_detail = obj.userbasicdetail.first()
        return user_basic_detail.city if user_basic_detail else None

    def get_member_status(self, obj):
        user_basic_detail = UserPurchaseOrderDetails.objects.filter(user=obj).first()
        return user_basic_detail.member_status if user_basic_detail else None

    def get_invested_amount(self, obj):
        total_invested_amount = (
            UserPurchaseOrderDetails.objects.filter(user=obj).aggregate(
                models.Sum("invested_amount")
            )["invested_amount__sum"]
            or 0.0
        )
        return total_invested_amount

    def get_current_value(self, obj):
        total_current_value = (
            UserPurchaseOrderDetails.objects.filter(user=obj).aggregate(
                models.Sum("current_value")
            )["current_value__sum"]
            or 0.0
        )
        return total_current_value
    def get_kyc_status(self,obj):
        user_basic_detail = obj.userbasicdetail.first()
        return user_basic_detail.verification if user_basic_detail else None
    def get_portfolio_no(self,obj):
        user_basic_detail = UserPurchaseOrderDetails.objects.filter(user=obj).first()
        return user_basic_detail.portfolio_no if user_basic_detail else None



# serializers for comlete user details


class UserAllDetailsSerializer(serializers.ModelSerializer):
    invested_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "profile_photo",
            "username",
            "email",
            "phone_no",
            "verification",
            "invested_amount",
        ]

    def get_invested_amount(self, obj):
        total_invested_amount = (
            UserPurchaseOrderDetails.objects.filter(user=obj).aggregate(
                models.Sum("invested_amount")
            )["invested_amount__sum"]
            or 0.0
        )
        return total_invested_amount

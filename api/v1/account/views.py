from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.generics import ListAPIView
import random
from django.contrib.auth import get_user_model
from .models import (
    User,
    UserBasicDetail,
    PanVerification,
    AdharCardVerify,
    SIP,
    UserPurchaseOrderDetails,
)
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserChangePasswordSerializer,
    SendResetPasswordEmailSerializer,
    UserResetPasswordSerializer,
    UserProfileSerializer,
    UserBasicDetailSerializer,
    UserPanVerification,
    UserAdharVerification,
    UserPurchaseOrderSerializer,
    UserDetailsSerializer,
    UserAllDetailsSerializer,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate
from .renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from api.v1.mutual_sip.models import SIP


# jwt token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# user registration
class UserRegistration(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {
                "success": True,
                "msg": "user is registered successfully",
                "token": token,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# user login
class UserLogin(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)
        if user.is_blocked == False:
            if user is not None:
                details = get_user_model().objects.get(email=email)
                user_detail = {
                    "username": details.username,
                    "email": details.email,
                    "id": details.id,
                    "phone_no": details.phone_no,
                    "referral_code": details.referral_code,
                }
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "success": True,
                        "msg": "login user successfully",
                        "token": token,
                        "user": user_detail,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["your email or password is not valid"]
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {"errors": {"non_field_errors": ["you are blocked"]}},
                status=status.HTTP_403_FORBIDDEN,
            )


# user change password
class UserChangePassword(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get("password")
        password1 = serializer.data.get("password1")
        password2 = serializer.data.get("password2")
        email = request.user.email
        print(email)
        user = authenticate(email=email, password=password)
        if user is not None:
            if password1 != password2:
                return Response({"msg": "password and confirm password are not same"})
            else:
                user.set_password(password1)
                user.save()
                return Response(
                    {"success": True, "msg": "password is changed successfully"},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response({"msg": "old password is not correct"})


# send  reset  password email
class SendPasswordResetEmail(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, **kwargs):
        serializer = SendResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data.get("otp")
            user_id = serializer.validated_data.get("id")
            return Response(
                {
                    "msg": "password reset link is sent to your registered email",
                    "otp": otp,
                    "user_id": user_id,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# reset password


class ResetPassword(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, pk, otp, **kwargs):
        serializer = UserResetPasswordSerializer(
            data=request.data, context={"id": pk, "otp": otp}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "password reset successully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get user's profile
class UserProfile(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, format=None):
        data = User.objects.all()
        serializer = UserProfileSerializer(data, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# change user's profile details
class ChangeUserProfile(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        data = User.objects.get(pk=pk)
        serializer = UserProfileSerializer(data, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                    "msg": "user personal info is changed successfully",
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk, format=None):
        data = User.objects.get(pk=pk)
        data.delete()
        return Response(
            {"success": True, "msg": "user personal info is deleted succcessfully"},
            status=status.HTTP_200_OK,
        )

    def get(self, request, pk=None, format=None):
        if pk is not None:
            data = User.objects.get(pk=pk)
            # if data==request.user:
            serializer = UserProfileSerializer(data)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            data = request.user
            serializer = UserProfileSerializer(data)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )


#  post user basic details
class PostUserBasicDetail(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserBasicDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "success": True,
                "msg": "user basic info is saved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# get all users basic details
class GetAllUserBasicDetail(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, format=None):
        data = UserBasicDetail.objects.all()
        serializer = UserBasicDetailSerializer(data, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# change user's basic details
class ChangeUserBasicDetails(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        data = UserBasicDetail.objects.get(pk=pk)
        serializer = UserBasicDetailSerializer(data, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                    "msg": "user basic info is changed successfully",
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk, format=None):
        data = UserBasicDetail.objects.get(pk=pk)
        data.delete()
        return Response(
            {"success": True, "msg": "user basic info is deleted succcessfully"},
            status=status.HTTP_200_OK,
        )

    def get(self, request, pk=None, format=None):
        data = UserBasicDetail.objects.get(pk=pk)
        serializer = UserBasicDetailSerializer(data)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


#  post user pan details
class PostUserPanDetail(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserPanVerification(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(
            {
                "success": True,
                "msg": "user pan info is saved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# get all users pan details
class GetAllUserPanDetail(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, format=None):
        data = PanVerification.objects.all()
        serializer = UserPanVerification(data, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# change user's pan details
class ChangeUserPanDetails(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        data = PanVerification.objects.get(pk=pk)
        serializer = UserPanVerification(data, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                    "msg": "user pan info is changed successfully",
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk, format=None):
        data = PanVerification.objects.get(pk=pk)
        data.delete()
        return Response(
            {"success": True, "msg": "user pan info is deleted succcessfully"},
            status=status.HTTP_200_OK,
        )

    def get(self, request, pk=None, format=None):
        data = PanVerification.objects.get(pk=pk)
        serializer = UserPanVerification(data)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


#  post user adhar details
class PostUserAdharDetail(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserAdharVerification(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(
            {
                "success": True,
                "msg": "user adhar info is saved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# get all users adhar details
class GetAllUserAdharDetail(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, format=None):
        data = AdharCardVerify.objects.all()
        serializer = UserAdharVerification(data, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# change user's adhar details
class ChangeUserAdharDetails(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        data = AdharCardVerify.objects.get(pk=pk)
        serializer = UserAdharVerification(data, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                    "msg": "user adhar info is changed successfully",
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk, format=None):
        data = AdharCardVerify.objects.get(pk=pk)
        data.delete()
        return Response(
            {"success": True, "msg": "user adhar info is deleted succcessfully"},
            status=status.HTTP_200_OK,
        )

    def get(self, request, pk=None, format=None):
        data = AdharCardVerify.objects.get(pk=pk)
        serializer = UserAdharVerification(data)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


#  post user sip's order details


class PostUserSipDetail(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        new_sip_id = request.data.get("sips")
        new_sip_ids = []
        new_sip_ids.append(new_sip_id)
        new_sips = SIP.objects.filter(id__in=new_sip_ids)
        serializer = UserPurchaseOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_purchase_order = serializer.save(user=self.request.user)
        if new_sips.exists():
            user_purchase_order.sips = new_sips.first()
            user_purchase_order.save()
        user_purchase_order.portfolio_no = random.randrange(100000000, 1000000000)
        user_purchase_order.sip_price = new_sips.first().current_value
        user_purchase_order.save()
        return Response(
            {
                "success": True,
                "msg": "User SIP info is saved successfully",
                "data": {
                    "user_purchase_order": serializer.data,
                },
            },
            status=status.HTTP_201_CREATED,
        )


# get all user's sip order details
class GetAllUserSipDetail(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, format=None):
        data = UserPurchaseOrderDetails.objects.all()
        serializer = UserPurchaseOrderSerializer(data, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# change user's order details
class ChangeUserSipDetails(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        try:
            data = UserPurchaseOrderDetails.objects.get(pk=pk)
            serializer = UserPurchaseOrderSerializer(
                data, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "data": serializer.data,
                        "msg": "user sip order info is changed successfully",
                    },
                    status=status.HTTP_200_OK,
                )
        except UserPurchaseOrderDetails.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, pk, format=None):
        data = UserPurchaseOrderDetails.objects.get(pk=pk)
        data.delete()
        return Response(
            {"success": True, "msg": "user sip order info is deleted succcessfully"},
            status=status.HTTP_200_OK,
        )

    def get(self, request, pk=None, format=None):
        try:
            data = UserPurchaseOrderDetails.objects.get(pk=pk)
            print(data)
            serializer = UserPurchaseOrderSerializer(data)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except UserPurchaseOrderDetails.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class GetSipThroughId(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        try:
            queryset = UserPurchaseOrderDetails.objects.filter(user=pk)
            instances = queryset.all()
            serializer = UserPurchaseOrderSerializer(
                instances, many=True
            )  # Fetch related user objects

            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except UserPurchaseOrderDetails.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserDetailsAPIView(ListAPIView):
    renderer_classes = [UserRenderers]
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        return queryset


class UserAllDetailsAPIView(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            order = UserPurchaseOrderDetails.objects.filter(user=user)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserAllDetailsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserSipPurchaseDetailthroughId(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, pk=None, format=None):
        try:
            queryset = UserPurchaseOrderDetails.objects.filter(user=pk)
            user_personal_detail = User.objects.get(id=pk)
            instances = queryset.all()
            serializer = UserPurchaseOrderSerializer(instances, many=True)

            sips_list = [item["sips"] for item in serializer.data]
            sips = [SIP.objects.get(id=item) for item in sips_list]
            total_invested_amount_of_user = [
                item["invested_amount"] for item in serializer.data
            ]
            current_values = [sip.current_value for sip in sips]
            gain_value = [sip.gain_value for sip in sips]
            name = [sip.name for sip in sips]
            annual_return_rate = [sip.annual_return_rate for sip in sips]
            for i, item in enumerate(serializer.data):
                item["current_value"] = current_values[i]
            for i, item in enumerate(serializer.data):
                item["gain_value"] = gain_value[i]
            for i, item in enumerate(serializer.data):
                item["annual_return_rate"] = annual_return_rate[i]
            for i, item in enumerate(serializer.data):
                item["sip_name"] = name[i]
            total_current_value = sum(current_values)
            total_invested_amount = sum(total_invested_amount_of_user)
            profile_photo_url = (
                user_personal_detail.profile_photo.url
                if user_personal_detail.profile_photo
                else None
            )

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                    "profile_photo": profile_photo_url,
                    "username": user_personal_detail.username,
                    "email": user_personal_detail.email,
                    "kyc_status": user_personal_detail.verification,
                    "total_current_value": total_current_value,
                    "total_investment": total_invested_amount,
                },
                status=status.HTTP_200_OK,
            )
        except UserPurchaseOrderDetails.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

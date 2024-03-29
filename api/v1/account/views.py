from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound
import random
from django.contrib.auth import get_user_model
from .models import (
    User,
    UserBasicDetail,
    PanVerification,
    AdharCardVerify,
    SIP,
    UserPurchaseOrderDetails,
    PreviousCurrentValueLog,
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
    PreviousCurrentValueLogSerializer,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate
from .renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from api.v1.mutual_sip.models import SIP
from api.v1.mutual_sip.serializers import SIPSerializer
from api.v1.payment.models import Transactions
from api.v1.payment.serializers import TransactionSerializer


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
from api.v1.account.models import User


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

        # Convert 'user' value to an integer
        check_user_exists = int(request.data.get("user"))

        # Retrieve the User instance corresponding to the user ID
        user_instance = User.objects.get(pk=check_user_exists)

        find_user = UserPurchaseOrderDetails.objects.filter(user=user_instance)

        # Initialize user_purchase_order
        user_purchase_order = None

        if find_user:
            old_portfolio = find_user.first().portfolio_no
            user_purchase_order = serializer.save(
                user=user_instance
            )  # Assign user instance
            user_purchase_order.portfolio_no = old_portfolio

        if new_sips.exists():
            # Ensure user_purchase_order is initialized if not found previously
            if not user_purchase_order:
                user_purchase_order = serializer.save(user=user_instance)
            user_purchase_order.sip_price = new_sips.first().min_amount
            user_purchase_order.save()

        if not find_user:
            # Ensure user_purchase_order is initialized if not found previously
            if not user_purchase_order:
                user_purchase_order = serializer.save(user=user_instance)
            user_purchase_order.portfolio_no = random.randrange(100000000, 1000000000)
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

    def patch(self, request, pk, format=None):
        try:
            instance = UserPurchaseOrderDetails.objects.get(pk=pk)
            serializer = UserPurchaseOrderSerializer(
                instance, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                # Manually fetch logs associated with the instance
                logs = PreviousCurrentValueLog.objects.filter(
                    user_purchase_order=instance
                )
                logs_serializer = PreviousCurrentValueLogSerializer(logs, many=True)

                # Add logs data to the serialized data
                serialized_data = serializer.data
                serialized_data["logs"] = logs_serializer.data

                return Response(
                    {
                        "success": True,
                        "data": serialized_data,
                        "msg": "current value is changed successfully",
                    },
                    status=status.HTTP_200_OK,
                )
        except UserPurchaseOrderDetails.DoesNotExist:
            raise NotFound(detail="User sip doesn't exist")

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


# user's all details
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


# get all details of user through purchase id
class GetUserSipPurchaseDetailthroughId(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, pk=None, format=None):
        try:
            users_in_sip = UserPurchaseOrderDetails.objects.filter(user=pk)
            total_investment = sum(
                user_sip.invested_amount for user_sip in users_in_sip
            )
            current_value = sum(user_sip.current_value for user_sip in users_in_sip)
            total_gain = current_value - total_investment
            queryset = UserPurchaseOrderDetails.objects.filter(user=pk)
            user_personal_detail = User.objects.get(id=pk)
            instances = queryset.all()
            serializer = UserPurchaseOrderSerializer(instances, many=True)
            # Get user profile photo URL
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
                    "total_current_value": current_value,
                    "total_investment": total_investment,
                    "total_gain": total_gain,
                },
                status=status.HTTP_200_OK,
            )
        except UserPurchaseOrderDetails.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


# get all details of all user
class GetUserAllPersonlDetails(APIView):
    def get(self, request, format=None):
        try:
            # Fetch all users
            all_users = User.objects.all()

            # Serialize user details for each user
            user_details = UserDetailsSerializer(all_users, many=True).data

            # Return response
            return Response(
                {"success": True, "data": user_details}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# get a single user's all details


class GetUserAllDetailsThroughUserId(APIView):
    def get(self, request, pk=None, format=None):
        try:
            # Fetch the user based on the provided pk
            user = User.objects.get(pk=pk)
            sip_details = UserPurchaseOrderDetails.objects.filter(user=user)

            # Serialize user details
            user_details = UserDetailsSerializer(user).data
            profit = user_details.get("current_value", 0) - user_details.get(
                "invested_amount", 0
            )
            user_details["profit"] = profit

            # Initialize dictionary to store SIP details
            sip_data_dict = {}

            # Fetch SIP details for each purchase order
            for sip_detail in sip_details:
                sip = sip_detail.sips
                total_investment = sip_detail.invested_amount
                current_value = sip_detail.current_value

                # Serialize SIP details
                sip_data = SIPSerializer(sip).data
                sip_data["total_investment"] = total_investment
                sip_data["current_value"] = current_value
                sip_data["total_gain"]=current_value-total_investment

                # Add SIP details to dictionary
                sip_data_dict[sip.id] = sip_data

            queryset = Transactions.objects.filter(user=pk)
            instances = queryset.all()
            serializer = TransactionSerializer(instances, many=True)

            # Return response
            return Response(
                {
                    "success": True,
                    "user_details": user_details,
                    "sips": list(sip_data_dict.values()),
                    "transactions": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"success": False, "msg": "User with the provided id does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"success": False, "msg": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

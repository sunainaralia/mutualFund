from rest_framework.response import Response
from rest_framework import status
import json
from .models import User, UserBasicDetail, PanVerification, AdharCardVerify
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
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate
from .renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated


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
            {"success": True, "msg": "user is registered successfully", "token": token},
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
        if user is not None:
            details = User.objects.get(email=email)
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
            return Response(
                {"msg": "password reset link is sent to your registered email"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# reset password


class ResetPassword(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, uid, token, **kwargs):
        serializer = UserResetPasswordSerializer(
            data=request.data, context={"uid": uid, "token": token}
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
            # else:
            #      return Response({"success": False, "data": serializer.data}, status=status.HTTP_200_OK)
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
        user=request.user
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

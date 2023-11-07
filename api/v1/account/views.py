from rest_framework.response import Response
from rest_framework import status
import json
from .models import User
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserChangePasswordSerializer,SendResetPasswordEmailSerializer,UserResetPasswordSerializer,UserProfileSerializer
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
                "phone_no":details.phone_no,
                "referral_code":details.referral_code}
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
    permission_classes=[IsAuthenticated]
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
        
#send  reset  password email
class SendPasswordResetEmail(APIView):
        renderer_classes=[UserRenderers]
        def post(self, request, **kwargs):
            serializer=SendResetPasswordEmailSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                return Response({'msg':'password reset link is sent to your registered email'},status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
# reset password
        
class ResetPassword(APIView):
    renderer_classes=[UserRenderers]
    def post(self,request,uid,token,**kwargs):
        serializer=UserResetPasswordSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset successully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
# user's profile
class UserProfile(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )
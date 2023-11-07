from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.authentication import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
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
            "profile_photo"
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
class SendResetPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            body='click following link to reset your password'+link
            print(body)
            data={
                'subject':'Reset your password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("this email is not registered")

# password reset serializer
class UserResetPasswordSerializer(serializers.Serializer):
    password1=serializers.CharField(style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password1','password2']
    def validate(self, attrs):
            password1=attrs.get('password1')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if password1!=password2:
                raise serializers.ValidationError("password and confirm password are not matched") 
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("token is expired or not valid")
            user.set_password(password1)
            user.save()
            return attrs
      

# serializer for user profile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username","phone_no","referral_code","profile_photo"]
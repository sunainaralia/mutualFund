from django.urls import path
from api.v1.account.views import UserRegistration,UserLogin,UserChangePassword,SendPasswordResetEmail,ResetPassword,UserProfile
urlpatterns = [
    path('registration/',UserRegistration.as_view()),
    path('login/',UserLogin.as_view()),
    path('changepassword/',UserChangePassword.as_view()),
    path('sendresetemail/',SendPasswordResetEmail.as_view()),
    path('resetpassword/<uid>/<token>/',ResetPassword.as_view()),
    path('profile/',UserProfile.as_view()),
]
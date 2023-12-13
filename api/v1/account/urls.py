from django.urls import path
from api.v1.account.views import (
    UserRegistration,
    UserLogin,
    UserChangePassword,
    SendPasswordResetEmail,
    ResetPassword,
    UserProfile,
    ChangeUserProfile,
    GetAllUserBasicDetail,
    PostUserBasicDetail,
    ChangeUserBasicDetails,
    GetAllUserPanDetail,
    PostUserPanDetail,
    ChangeUserPanDetails,
    GetAllUserAdharDetail,
    PostUserAdharDetail,
    ChangeUserAdharDetails,
    PostUserSipDetail,
    GetAllUserSipDetail,
    ChangeUserSipDetails,
)

urlpatterns = [
    path("registration/", UserRegistration.as_view()),
    path("login/", UserLogin.as_view()),
    path("changepassword/", UserChangePassword.as_view()),
    path("sendresetemail/", SendPasswordResetEmail.as_view()),
    path("resetpassword/<pk>/<otp>/", ResetPassword.as_view()),
    path("profile/", UserProfile.as_view()),
    path("changeprofile/<pk>/", ChangeUserProfile.as_view()),
    path("basicall/", GetAllUserBasicDetail.as_view()),
    path("basicpost/", PostUserBasicDetail.as_view()),
    path("changebasic/<pk>/", ChangeUserBasicDetails.as_view()),
    path("panall/", GetAllUserPanDetail.as_view()),
    path("panpost/", PostUserPanDetail.as_view()),
    path("changepan/<pk>/", ChangeUserPanDetails.as_view()),
    path("adharall/", GetAllUserAdharDetail.as_view()),
    path("adharpost/", PostUserAdharDetail.as_view()),
    path("changeadhar/<pk>/", ChangeUserAdharDetails.as_view()),
    path("sippost/", PostUserSipDetail.as_view()),
    path("sipall/", GetAllUserSipDetail.as_view()),
    path("changesip/<pk>/", ChangeUserSipDetails.as_view()),
]

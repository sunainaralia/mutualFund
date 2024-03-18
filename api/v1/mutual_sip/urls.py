# mutual_fund_app/urls.py
from django.urls import path, include
from .views import (
    PostSip,
    GetAllSip,
    ChangeSip,
    PostSipDetails,
    ChangeSipDetails,
    GetAllSipDetails,
)

urlpatterns = [
    path("sip/", PostSip.as_view(), name="sip-list-create"),
    path(
        "sip/<int:pk>/",
        ChangeSip.as_view(),
        name="sip-retrieve-update-destroy",
    ),
    path("allsip/", GetAllSip.as_view()),
    path("sipdetails/", PostSipDetails.as_view(), name="sip-list-details-create"),
    path(
        "sipdetails/<int:pk>/",
        ChangeSipDetails.as_view(),
        name="sip-retrieve-details-update-destroy",
    ),
    path("allsipdetails/", GetAllSipDetails.as_view()),
]

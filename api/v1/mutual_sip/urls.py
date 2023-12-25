# mutual_fund_app/urls.py
from django.urls import path,include
from .views import PostSip, GetAllSip, ChangeSip

urlpatterns = [
    path("sip/", PostSip.as_view(), name="sip-list-create"),
    path(
        "sip/<int:pk>/",
        ChangeSip.as_view(),
        name="sip-retrieve-update-destroy",
    ),
    path("allsip/", GetAllSip.as_view()),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.response import Response
from rest_framework.views import APIView


class welcomeApi(APIView):

    def get(self, request, pk=None, format=None):
        return Response({"msg": "welcome to mutual fund"})


urlpatterns = [
    path("", welcomeApi.as_view()),
    path("admin/", admin.site.urls),
    path("user/", include("api.v1.account.urls")),
    path("api/", include("api.v1.mutual_sip.urls")),
    path("payment/", include("api.v1.payment.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

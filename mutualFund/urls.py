from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("api.v1.account.urls")),
    path("api/", include("api.v1.mutual_sip.urls")),
    path("payment/", include("api.v1.payment.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

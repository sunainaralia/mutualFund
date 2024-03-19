# admin.py

from django.contrib import admin
from .models import SIP


class SIPAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "current_annual_return_rate",
        "created_at",
        "investment_type",
        "sip_status",
        "sip_photo",
        "annual_return_rate",
        "min_amount",
        "description",
        "time_period",
       
    ]


admin.site.register(SIP, SIPAdmin)

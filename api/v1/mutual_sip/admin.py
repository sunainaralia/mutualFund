# admin.py

from django.contrib import admin
from .models import SIP, SIP_DETAILS


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
    ]


admin.site.register(SIP, SIPAdmin)


class SIPDetailsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "no_of_investors",
        "min_amount",
        "current_value",
        "total_investment",
        "time_period",
        "sip",
        "gain_value",
    ]


admin.site.register(SIP_DETAILS, SIPDetailsAdmin)

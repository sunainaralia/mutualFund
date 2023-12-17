# admin.py

from django.contrib import admin
from .models import SIP


class SIPAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "current_annual_return_rate",
        "min_amount",
        "current_value",
        "time_period",
        "created_at",
        "total_investment",
        "investment_type",
        "sip_status",
        "gain_value",
        "no_of_investors",
        "sip_photo",
        "annual_return_rate",
    ]


admin.site.register(SIP, SIPAdmin)

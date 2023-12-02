from django.contrib import admin

from .models import SIP


# Register your models here.
class SipAdmin(admin.ModelAdmin):
    list_display = [
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
        "sip_users",
        "no_of_investors",
        "users",
    ]


admin.site.register(SIP, SipAdmin)

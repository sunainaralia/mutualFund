from django.contrib import admin

from .models import SIP


# Register your models here.
class SipAdmin(admin.ModelAdmin):
    list_display = [
        # "user",
        "name",
        "current_annual_return_rate",
        "min_amount",
        "current_value",
        "time_period",
        "created_at",
        "no_of_investers",
        "total_investment",
        "investment_type",
        "sip_status",
        "gain_value",
    ]


admin.site.register(SIP, SipAdmin)

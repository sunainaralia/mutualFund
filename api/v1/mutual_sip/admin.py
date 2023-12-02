# admin.py

from django.contrib import admin
from .models import SIP
from api.v1.account.models import UserSipDetails


class UserSipDetailsInline(admin.TabularInline):
    model = UserSipDetails
    extra = 1


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
        "usernames_of_users_taken",
    ]

    inlines = [UserSipDetailsInline]

    def usernames_of_users_taken(self, obj):
        return ", ".join(user.user.username for user in obj.sip_details.all())

    usernames_of_users_taken.short_description = "Usernames of Users Taken"


admin.site.register(SIP, SIPAdmin)

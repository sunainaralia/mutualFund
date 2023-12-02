from django.contrib import admin
from .models import (
    User,
    UserBasicDetail,
    PanVerification,
    AdharCardVerify,
    UserSipDetails,
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ["id", "email", "username", "is_admin", "phone_no", "referral_code"]
    list_filter = [
        "is_admin",
    ]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Personal info",
            {"fields": ["username", "phone_no", "referral_code", "profile_photo"]},
        ),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)


# user basic details
class UserBasicDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "nationality",
        "zip_code",
        "fullName",
        "d_o_b",
        "address_details",
        "state",
    ]


admin.site.register(UserBasicDetail, UserBasicDetailAdmin)


# user pan details
class UserPanDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "pan_card",
        "pan_no",
    ]


admin.site.register(PanVerification, UserPanDetailAdmin)


# user adhar details
class UserAdharDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "adhar_card_front", "adhar_no", "adhar_card_back", "user"]


admin.site.register(AdharCardVerify, UserAdharDetailAdmin)


# user sip details
class UserSipAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "invested_amount",
        "member_status",
        "gain_value",
        "user",
        "sips",
    ]


admin.site.register(UserSipDetails, UserSipAdmin)

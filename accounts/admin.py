from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserAgreement

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "avatar")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    agreement_columns = [
        ("terms", "이용약관"),
        ("privacy", "개인정보"),
        ("marketing", "마케팅"),
    ]

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        *[f"{key}_status" for key, _ in agreement_columns],
        "is_staff",
    )

    def get_agreement_status(self, user, agreement_type):
        return UserAgreement.objects.filter(
            user=user, agreement_type=agreement_type, agreed=True
        ).exists()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, label in self.agreement_columns:
            self._register_agreement_column(key, label)

    def _register_agreement_column(self, agreement_type, label):
        def status_method(self, obj):
            return self.get_agreement_status(obj, agreement_type)

        status_method.boolean = True
        status_method.short_description = label
        setattr(self.__class__, f"{agreement_type}_status", status_method)

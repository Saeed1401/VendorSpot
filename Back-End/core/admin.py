from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User



# admin.site.register(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ["date_joined"]
  
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", 
                                        "last_name", 
                                        "email", 
                                        "image", 
                                        "gender", 
                                        "language"
                                        )}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
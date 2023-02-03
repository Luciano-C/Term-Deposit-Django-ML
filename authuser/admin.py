from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
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

    # Esto es importante para crear usuarios con el modelo personalizado en la tabla de administración

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_display = ("email", "name", "is_staff")
    search_fields = ("name", "email")
    ordering = ["email"]


admin.site.register(User, CustomUserAdmin)



""" 
The parent class (django.contrib.auth.admin.UserAdmin) has an add_fieldsets attribute that includes the username field. Add an attribute to your MyUserAdmin class called add_fieldsets and treat it like the fieldsets attribute: use it to define fields you want to show in the add form.

Note: If your username is set to email then add email to add_fieldsets.

See the note about add_fieldset at the "Customizing authentication in Django" docs page and the full example from the Django docs.

Fuente: https://stackoverflow.com/questions/17196244/django-unknown-fields-username-specified-for-pouser
"""
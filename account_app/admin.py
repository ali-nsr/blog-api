from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'is_active', 'is_verified', 'is_superuser', 'created_date',)
    ordering = ('-created_date',)

    # fieldsets = (
    #     ('Authentication', {'fields': ('email', 'password',)}),
    #     # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    #     ('Dates', {'fields': ('last_login',)}),
    # )
    #
    # add_fieldsets = (
    #     (None, {'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser',)}),
    # )


admin.site.register(User, UserAdmin)
admin.site.register(Profile)

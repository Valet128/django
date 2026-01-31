from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('date_joined', 'email', 'last_name', 'first_name', 'middle_name', 'phone', 'address')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
    (None, {'fields': ('email', 'password')}),
    (_('Personal info'), {'fields': ('last_name', 'first_name', 'middle_name', 'phone', 'address', 'ip_address')}),
    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
    ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

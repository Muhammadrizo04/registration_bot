from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm, UserCreationForm
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'phone_number', 'email', 'password1', 'password2')


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('full_name', 'phone_number', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('full_name', 'phone_number')
    ordering = ('full_name',)
    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'phone_number', 'email', 'region', 'district', 'quarter')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'role'),
        }),
        ('Change Password', {
            'fields': ('password',),
            'classes': ('collapse',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'phone_number', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'role'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
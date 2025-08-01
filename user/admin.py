from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, OTP
from .forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username', 'email', 'created_at', 'is_admin']
    list_filter = ['is_admin', 'role', 'created_at']

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'password',
                'avatar',
                'role',
                'is_2fa_enabled',
                'balance'
            )
        }),
        ('Permissions', {
            'fields': ('is_admin',)
        }),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2'
            )
        }),
    )

    search_fields = ('username', 'email')
    filter_horizontal = ()

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')
    search_fields = ('user__email', 'code')
    ordering = ('-created_at',)
admin.site.register(MyUser, UserAdmin)
admin.site.register(OTP, OTPAdmin)
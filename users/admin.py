from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Customer, ServiceProvider, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'phoneNumber')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phoneNumber', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'phoneNumber', 'user_type', 'password1', 'password2', 'is_staff', 'is_active'),
            },
        ),
    )


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'isVerified')
    list_filter = ('isVerified',)
    search_fields = ('user__email',)

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return ('idProof',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)

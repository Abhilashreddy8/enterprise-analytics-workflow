
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'role', 'location', 'is_staff')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('role', 'location', 'lead')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'location', 'lead'),
        }),
    )

    search_fields = ('email',)


admin.site.register(User, CustomUserAdmin)
#admin.site.register(User)
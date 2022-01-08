from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import HotelManager


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """ attrs: is_superuser,is_active,is_staff (let op: no is_admin)"""
    search_fields = ('email', 'username')
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'username', 'last_login', 'is_active', 'is_superuser','is_hotel_manager')
    list_filter = ( 'is_active', 'is_superuser','is_hotel_manager')

    # add key 'classes' with value [collapse ] to toggle Permissions,Important Dates
    fieldsets = (
        (_('User'), {'fields': ('username', 'email', 'password', 'is_active')}),
        (_('Permissions'), {'classes': ['collapse'], 'fields': (
            'is_hotel_manager','is_superuser', 'groups', 'user_permissions',)}),
        (_('Important dates'), {'classes': ['collapse'], 'fields': ('last_login', 'date_joined')}),

    )    
    
    add_fieldsets = (
        (('Add Your User'), {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')



admin.site.register(User, UserAdmin)
admin.site.register(HotelManager)



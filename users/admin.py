from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import HotelManager
from .models import HotelManager

User = get_user_model()

admin.site.register(User)
admin.site.register(HotelManager)

# Register your models here.

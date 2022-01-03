from django.contrib import admin
from .models import City, Hotel
from .forms import CityForm


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    form = CityForm


admin.site.register(City)

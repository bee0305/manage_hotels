from django.contrib import admin
from .models import City, Hotel
from .forms import CityForm


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """"""
    form = CityForm
    list_display = ('id','name','unid','city_code')
    list_filter = ( 'city',)


@admin.register(City)
class CityForm(admin.ModelAdmin):
    list_display = ('id','name','city_code')



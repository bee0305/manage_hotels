from django.contrib import admin
from .models import City, Hotel
from .forms import CityForm


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    form = CityForm
    list_display = ('id','name','unid','short_cut')
    list_filter = ( 'city',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name')



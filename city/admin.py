from django.contrib import admin
import django.apps
from .models import City, Hotel
from .forms import CityForm
from users.models import HotelManager

# models = django.apps.apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         print('already registered')
# admin.site.unregister(django.contrib.sessions.models.Session)

TIP ='Enter 3 chars to start search'

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """"""
    form = CityForm
    list_display = ('id','name','unid','city_code','get_city_name')
    list_filter = ( 'city',)
    fieldsets = (
        ('Section 1:Meta data',{
            'fields':('city_code','unid'), 
            'classes':('collapse',)
        }),
        ('Section 2: Hotel Name',{
            'fields':('name',)
        }),
        ('Section 3: search for city',{
            'fields':('city',),
            'description':f'{TIP}'
        })
        
    )
    def get_city_name(self,obj):
        return obj.city.name

    get_city_name.short_description = 'City Name'  
    # can be sorted
    get_city_name.admin_order_field = 'city'      

@admin.register(City)
class CityForm(admin.ModelAdmin):
    list_display = ('id','name','city_code','get_city_hotel_manager')

    def get_city_hotel_manager(self,obj):
        if obj.managers.first():
            return obj.managers.first()
        else:
            return 'No manager yet'    
    get_city_hotel_manager.short_description = 'City Manager'    


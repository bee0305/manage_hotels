from django.urls import path
from .views import load_cities, load_hotels, CityListView,get_city_hotels,get_city_hotels2


app_name = 'city'

urlpatterns = [
    path('',load_cities,name='load-cities'),   
    path('hotels/',load_hotels,name='load-hotels'),  
    path('show-all-cities/',CityListView.as_view(),name='all-cities'),
    path('city-hotels/<city_name>/',get_city_hotels,name='city-hotels'), 
    path('city-hotels2/',get_city_hotels2,name='city-hotels2') 
    
]
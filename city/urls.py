from django.urls import path
from .views import load_cities, load_hotels, CityListView, get_city_hotels, get_city_hotels_search

app_name = 'city'

urlpatterns = [
    path('', load_cities, name='load-cities'),
    path('hotels/', load_hotels, name='load-hotels'),
    path('show-all-cities/', CityListView.as_view(), name='all-cities'),
    path('city-hotels/<city_name>/', get_city_hotels, name='city-hotels'),
    path('city-hotels-search/', get_city_hotels_search, name='city-hotels-search')

]

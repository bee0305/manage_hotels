from django.urls import path
from .views import (load_cities, load_hotels, CityListView, get_city_hotels, 
                    get_city_hotels_search,ManageCity)

app_name = 'city'

urlpatterns = [
    path('', load_cities, name='load-cities'),
    path('hotels/', load_hotels, name='load-hotels'),
    path('show-all-cities/', CityListView.as_view(), name='all-cities'),
    path('city-hotels/<city_name>/', get_city_hotels, name='city-hotels'),
    path('city-hotels-search/', get_city_hotels_search, name='city-hotels-search'),
    path('manage-city/',ManageCity.as_view(),name='manage-city'),

]

htmx_urlpatterns = [
    path('add-new-hotel/', ManageCity.as_view(), name='add-new-hotel'),
    path('delete-hotel/<int:pk>', ManageCity.as_view(), name='delete-hotel')
    
]

urlpatterns += htmx_urlpatterns

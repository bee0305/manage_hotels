from django.urls import path
from .views import (CityListView, HXManageCity,ManageCity,get_city_hotels, load_cities, load_hotels, 
                    get_city_hotels_search,get_hotel_detail,start_hotel_edit,clear )

app_name = 'city'

urlpatterns = [
    path('', load_cities, name='load-cities'),
    path('hotels', load_hotels, name='load-hotels'),
    path('show-all-cities', CityListView.as_view(), name='all-cities'),
    path('city-hotels/<city_name>', get_city_hotels, name='city-hotels'),
    path('city-hotels-search', get_city_hotels_search, name='city-hotels-search'),

]

htmx_urlpatterns = [
    path('manage-hotels/<action>/<city_slug>',HXManageCity.as_view(),name='manage-hotels'),   
    path('hx-get-hotel-detail/<unid>/', get_hotel_detail, name='hotel-detail'),   
    path('hx-start-edit-hotel/<unid>/<city_slug>', start_hotel_edit, name='start-edit-hotel'),
    path('hx-finish-hotel-edit/<unid>/<city_slug>', HXManageCity.as_view(), name='edit-hotel'),
    path('hx-add-new-hotel/<city_slug>', HXManageCity.as_view(), name='add-new-hotel'),    
    path('hx-delete-hotel/<int:pk>/<city_slug>', HXManageCity.as_view(), name='delete-hotel'),
    path('hx-city-hotels-search', ManageCity.as_view(), name='hx-hotels-search'),
    path('clear',clear,name='clear')
    
    
]

urlpatterns += htmx_urlpatterns

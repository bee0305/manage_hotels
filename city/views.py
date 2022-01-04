import json
from django.conf import settings
from django.db.models import manager
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import JsonResponse

from city.forms import SearchForm
from users.models import HotelManager
from .models import City, Hotel
from .forms import SearchForm
from utils.request_help import make_request_cities, make_request_hotels_slow


def load_cities(request, url=settings.CITY_URL):
    """ 
    make a get request via simple auth to fetch a list of cities and create db records
    of City objects
    """
    make_request_cities(url)
    return render(request, 'cities/show_cities.html')


def load_hotels(request, url=settings.HOTEL_URL):
    """ 
    make a get request via simple auth to fetch a list of hotels  and create db records
    of Hotel objects
    """
    make_request_hotels_slow(url)
    return render(request, 'cities/show_cities.html')


class CityListView(ListView):
    """ display list of cites objects with a search form (incl autocomplete module dj-ajax-select)"""
    model = City
    context_object_name = 'cities'
    template_name = 'cities/show_cities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_city_form = SearchForm()
        context['search_city_form'] = search_city_form
        return context


def get_city_hotels(request, city_name):
    """
    func for ajax request from city list: via a tag with city name;
    return a list of filtered hotels for a chosen city to render on the same page    
    """
    if city_name:
        city = get_object_or_404(City, name=city_name)
        hotels = Hotel.objects.select_related('city').filter(city=city)
        data = [{'name': hotel.name, 'id': hotel.id} for
                hotel in hotels]
        json_city_name = json.dumps({"city": city_name})
        json_hotel_data = json.dumps(data)
        data = {"hotels": json_hotel_data, "city": json_city_name}
        return JsonResponse(data)
    else:
        print('no city name found')


def get_city_hotels_search(request):

    """
    func for ajax request from city list: via a search form with dj-ajax-select module;
    return a list of filtered hotels for a chosen city to render on the same page    
    """

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data['city']
            city = get_object_or_404(City, name=city.name)
            hotels = Hotel.objects.select_related('city').filter(city=city)
            json_city_name = json.dumps({"city": city.name})
            json_hotel_data = [{'name': hotel.name, 'id': hotel.id} for
                               hotel in hotels]
            data = {"hotels": json_hotel_data, "city": json_city_name}
            return JsonResponse(data)
        else:
            print('form is invalid')
            return JsonResponse({"data": "invalid"})


class ManageCity(LoginRequiredMixin,UserPassesTestMixin, View):

    def test_func(self):
        # print(self.request.user.is_hotel_manager)
        return self.request.user.is_hotel_manager

    def get(self,request,*args,**kwargs):             
        manager = HotelManager.objects.filter(user=request.user).last()
        city = manager.city
        hotels = city.hotels.all().order_by('name')          
        return render(request,'cities/manage_city.html',{'city':city.name,'hotels':hotels})

    def post(self,request,*args,**kwargs):  
        #  "ANT";"ANT11";"Agora"  short_cut;unid;name     
        print('kwargs',kwargs)
        print('args',args)
        hotel_name = request.POST.get('hotelname')
        manager =  HotelManager.objects.filter(user=request.user).last()    
        city = manager.city
        new_hotel = Hotel.objects.get_or_create(city=city,name=hotel_name,)[0]
        hotels = city.hotels.all().order_by('name')
        return render(request, '_partials/list_hotels.html', {'hotels':hotels})

    
    
    def delete(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        print('id is:',id)
        manager =  HotelManager.objects.filter(user=request.user).last()    
        city = manager.city
        hotels = city.hotels.all().order_by('name')
        return render(request, '_partials/list_hotels.html', {'hotels':hotels})

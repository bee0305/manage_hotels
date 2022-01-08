import json
from django.conf import settings

from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import JsonResponse

from city.forms import SearchForm
from users.models import HotelManager
from .models import City, Hotel
from .forms import SearchForm,HotelForm
from utils.request_help import make_request_cities, make_request_hotels_slow


def load_cities(request, url=settings.CITY_URL):
    """ 
    make a get request via simple auth to fetch a list of cities and create db records
    of City objects
    """
    make_request_cities(url)
    print('Cities req done')
    return render(request, 'cities/api_requests.html',{'msg':'api request cities done'})


def load_hotels(request, url=settings.HOTEL_URL):
    """ 
    make a get request via simple auth to fetch a list of hotels  and create db records
    of Hotel objects
    """
    make_request_hotels_slow(url)
    print('hotel req done')
    return render(request, 'cities/api_requests.html',{'msg':'api request hotels  done'})


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
        ctx = {'city':city.name}       
            
        return render(request,'cities/manage_city.html',ctx)      

class HXManageCity(LoginRequiredMixin,UserPassesTestMixin, View): 
    """ htmx get and post requests with check hotel manager """

    def test_func(self):        
        return self.request.user.is_hotel_manager       

    def get(self,request,*args,**kwargs):  
        """
        expect kwargs=='action' in url|=> return 
        # empty hotel form
        # list of corresponding hotel 
        # start page for manager
        # NOT incl hotel detail (see another func)
        """           
        manager = HotelManager.objects.filter(user=request.user).last()
        city = manager.city        
        action = kwargs.get('action') 
        if action =='form':            
            hotel_form = HotelForm()       
            ctx = {'hotel_form':hotel_form}     
            return render(request,'_partials/hotel_form.html',ctx)
        else: 
            hotels = city.hotels.all().order_by('name')                           
            if action == 'start':                
                ctx = {'city':city,'hotels':hotels} 
                return render(request,'cities/manage_city.html',ctx)   
            elif action == 'hotels': 
                ctx = {'hotels':hotels}     
                return render(request,'_partials/list_hotels.html',ctx)           
            
    def post(self,request,*args,**kwargs):  
        #  "ANT";"ANT11";"Agora"  city_code;unid;name    
        manager =  HotelManager.objects.filter(user=request.user).last()    
        city = manager.city
        unid= kwargs.get('unid') 
        if unid:
            # edit existed object hotel
            obj = Hotel.objects.get(unid=unid)            
            hotel_form = HotelForm(request.POST,instance=obj)
            if hotel_form.is_valid():                
                hotel = hotel_form.save()
                return render(request, '_partials/hotel_detail.html', {'hotel':hotel})
            else:
                # show form with errors
                return render(request, '_partials/hotel_form.html', {'hotel_form':hotel_form,'flag':'errors'})     
        else: 
            # create new object hotel            
            hotel_form = HotelForm(request.POST)            
            if hotel_form.is_valid():
                print('form is valid') 
                hotel = hotel_form.save(commit=False)                
                hotel.city = city
                hotel.save()
                return render(request, '_partials/hotel_detail.html', {'hotel':hotel})
            else:
                print('err in form') 
                return render(request, '_partials/hotel_form.html', {'hotel_form':hotel_form})  
                              
    
    def delete(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        print('id is:',id)
        manager =  HotelManager.objects.filter(user=request.user).last()    
        city = manager.city
        try:
            Hotel.objects.get(id=id,city=city).delete()            
            hotels = city.hotels.all().order_by('name')
            return render(request, '_partials/list_hotels.html',{'hotels':hotels})            
        except Exception as e:
            print('obj not found') 
            print(e)            
            return render(request, '_partials/404.html')  
        


def get_hotel_detail(request,unid): 
    #  "ANT";"ANT11";"Agora"  city_code;unid;name 
    user = request.user
    if  user.is_hotel_manager:
        manager =  HotelManager.objects.filter(user=request.user).last()    
        city = manager.city
        try:
            hotel = Hotel.objects.get(unid=unid,city=city)
            return render(request, '_partials/hotel_detail.html',{'hotel':hotel})        
        except Exception as e:                      
            return render(request, '_partials/404.html')

def start_hotel_edit(request,unid): 
    #  return hotel form with intial vals     
    user = request.user
    if  user.is_hotel_manager:
        manager =  HotelManager.objects.filter(user=request.user).last()    
        city = manager.city
        try:
            hotel = Hotel.objects.get(unid=unid,city=city)
            print('hotel is',hotel,hotel.unid)
            hotel_form = HotelForm(instance=hotel)            
            return render(request, '_partials/hotel_form.html',
                    {'hotel_form':hotel_form,'hotel':hotel,'flag':'ZOOOOO'})        
        except Exception as e:
            print('obj not found') 
            print(e)            
            return render(request, '_partials/404.html')


from django.test import TestCase, Client
from django.urls import reverse
from city.models import Hotel, City
from users.models import HotelManager
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.city = City.objects.create(name='Zorro', city_code='zor')
        self.user = User.objects.create_user(username="Juliana",email = "juliana@dev.io")
        self.mrX_user = User.objects.create_user(username="boef",email = "mrX@boef.io")
        self.user.is_hotel_manager = True
        self.user.save()
        self.manager = HotelManager(user=self.user,city=self.city)
        self.manager.save()
        
        # GET requests with different kwrags('action')
        self.get_form_url = reverse('city:manage-hotels',kwargs={'action':'form'})
        self.get_start_manager_page = reverse('city:manage-hotels',kwargs={'action':'start'})

        self.hotel_one = Hotel.objects.create(name='Sport', city_code=self.city.city_code, unid='uiop', city=self.city)
        self.hotel_two = Hotel.objects.create(name='Season', city_code=self.city.city_code, unid='tyrf', city=self.city)
        

        # POST requests
        self.delete_url = reverse('city:delete-hotel',kwargs={'pk':self.hotel_one.id})
        
        self.add_url = reverse('city:add-new-hotel')
        
    def test_delete_hotel(self):
        """  
        if user auth-ed && is_hotel_manager && for a given city|=> 
        can delete hotel via DELETE request
        """        
        self.client.force_login(user=self.user)
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.delete(self.delete_url)  
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(inital_count_hotels,final_count_hotel)
        self.assertTemplateUsed(resp, '_partials/list_hotels.html')

    def test_add_hotel(self):
        """  
        if user auth-ed && is_hotel_manager && for a given city|=> 
        can add hotel via POST request
        """        
        self.client.force_login(user=self.user)
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.post(self.add_url,data={"name":"Rain","unid":"ankm","city":self.city})  
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(inital_count_hotels,final_count_hotel)
        self.assertTemplateUsed(resp, '_partials/hotel_detail.html')     
         
  
        
    def test_get_hotel_form(self):
        """  
        if user auth-ed && is_hotel_manager && for a given city|=> can ask for an empty form      
        """        
        self.client.force_login(user=self.user)
        resp = self.client.get(self.get_form_url)        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['hotel_form'].is_bound, False)
        self.assertTemplateUsed(resp, '_partials/hotel_form.html')

    def test_get_start_manager_page(self):
        """  
        if user auth-ed && is_hotel_manager && for a given city|=> can open start page for managers     
        """        
        self.client.force_login(user=self.user)
        resp = self.client.get(self.get_start_manager_page)        
        self.assertEqual(resp.status_code, 200)        
        self.assertTemplateUsed(resp, 'cities/manage_city.html')

    def test_deny_hotelform_user_not_manager(self):
        """  
        if user auth-ed but NOT is_hotel_manager can't get form to create a new hotel   
        """        
        self.client.force_login(user=self.mrX_user)
        resp = self.client.get(self.get_form_url)        
        self.assertEqual(resp.status_code, 403)  


    def test_deny_add_hotel_not_manger(self):
        """  
        if user auth-ed but NOT is_hotel_manager |=> 
        CAN NOT add hotel via POST request
        """        
        self.client.force_login(user=self.mrX_user)
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.post(self.add_url,data={"name":"Rain","unid":"ankm","city":self.city})  
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(inital_count_hotels,final_count_hotel)
             


     

from django.test import TestCase, Client
from django.urls import reverse
from city.models import Hotel, City
from users.models import HotelManager,User
from django.contrib.auth import get_user_model

User = get_user_model()

class TestViews(TestCase):
    fixtures =['city.json','users.json']

    def setUp(self):        
        self.client = Client()
        self.city= City.objects.get(id=6)  # Berlijn
        self.hotel = Hotel.objects.get(id=2331)
         
        # user not a manager             
        self.user_not_manager = User.objects.get(id=4)  
        # user is a manager but not for a given city     
        self.manager_other_city = User.objects.get(id=6)
        # user is superuser
        self.admin = User.objects.get(id=1)
        # user ids a city manager
        self.berlin_user = User.objects.get(id=9)
        
        # GET requests with different kwrags('action')
        self.get_form_url = reverse('city:manage-hotels',kwargs={'action':'form','city_slug':self.city.slug})
        self.get_start_manager_page = reverse('city:manage-hotels',kwargs={'action':'start','city_slug':self.city.slug})   

        self.edit_start_url = reverse('city:start-edit-hotel',kwargs={'city_slug':self.city.slug,'unid':self.hotel.unid}) 

        # POST requests               
        self.add_url = reverse('city:add-new-hotel',kwargs={'city_slug':self.city.slug}) 
        self.edit_finish_url = reverse('city:edit-hotel',kwargs={'unid':self.hotel.unid,'city_slug':self.city.slug,}) 


    def test_start_edit_hotel(self):
        """  
        if user auth-ed && is_hotel_manager && for a given city|=> 
        can start edit hotel via GET request (fetch form with current data)
        """        
        self.client.force_login(user=self.berlin_user)        
        resp = self.client.get(self.edit_start_url)              
        self.assertEqual(resp.status_code, 200)  
        self.assertTemplateUsed(resp, '_partials/hotel_form.html')         
        

    def test_finish_edit_hotel(self):
        """  
        if user auth-ed && is_hotel_manager && for a given city|=> 
        can edit hotel via POST request
        """        
        self.client.force_login(user=self.berlin_user)
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.post(self.edit_finish_url,data={"name":self.hotel.name,"unid":self.hotel.unid,"city":self.city})  
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(inital_count_hotels,final_count_hotel)
        self.assertTemplateUsed(resp, '_partials/hotel_detail.html')   

    def test_add_hotel(self):
        """  
        if user auth-ed && is_hotel_manager && for a given city|=> 
        can add hotel via POST request
        """        
        self.client.force_login(user=self.berlin_user)
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.post(self.add_url,data={"name":"Rain","unid":"ankm","city":self.city})  
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(inital_count_hotels,final_count_hotel)
        self.assertTemplateUsed(resp, '_partials/hotel_detail.html')       

    def test_city_manager_can_delete_hotel(self):
        """  
        if user auth-ed && and city manager|=> 
        can delete hotel via DELETE request
        """        
        self.client.force_login(user=self.berlin_user)
        # print(self.manager_other_city)
        hotel_to_delete = Hotel.objects.get(id=self.hotel.id)
        city_slug = hotel_to_delete.city.slug
        delete_url = reverse('city:delete-hotel',kwargs={'pk':hotel_to_delete.id,'city_slug':city_slug})        
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.delete(delete_url)  
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(inital_count_hotels,final_count_hotel)      
    
        
    def test_not_manager_cant_delete_hotel(self):
        """  
        if user auth-ed but not is_hotel_manager |=> 
        can't delete hotel via DELETE request
        """        
        self.client.force_login(user=self.user_not_manager)
        hotel_to_delete = Hotel.objects.get(id=2156)
        city_slug = hotel_to_delete.city.slug
        delete_url = reverse('city:delete-hotel',kwargs={'pk':hotel_to_delete.id,'city_slug':city_slug})
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.delete(delete_url)         
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 403)
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(inital_count_hotels,final_count_hotel)   
             
        

    def test_manager_for_another_city_can_NOT_delete_hotel(self):
        """  
        if user auth-ed && is_hotel_manager BUT not for a given city|=> 
        can NOT delete hotel via DELETE request
        """        
        self.client.force_login(user=self.manager_other_city)
        # print(self.manager_other_city)
        hotel_to_delete = Hotel.objects.get(id=self.hotel.id)
        city_slug = hotel_to_delete.city.slug
        delete_url = reverse('city:delete-hotel',kwargs={'pk':hotel_to_delete.id,'city_slug':city_slug})        
        inital_count_hotels = Hotel.objects.count()
        resp = self.client.delete(delete_url)  
        final_count_hotel = Hotel.objects.count()      
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(inital_count_hotels,final_count_hotel)

    
        

    
    
    

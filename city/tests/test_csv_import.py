from django.test import TestCase,Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_url = reverse('city:load-cities')           
          
    def test_get_ajax(self): 
        """test api point """
        response = self.client.get(self.api_url)  

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'cities/show_cities.html')
        


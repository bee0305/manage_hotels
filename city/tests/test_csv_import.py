import requests
from requests.auth import HTTPBasicAuth

from django.test import TestCase, Client
from django.conf import settings



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_url_cities = settings.CITY_URL
        self.api_url_hotels = settings.HOTEL_URL

    def test_get_ajax_cities(self):
        """test api point cities status Ok and template """
        response = requests.head(url=self.api_url_cities, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
        self.assertEqual(response.status_code, 200)
        

    def test_get_ajax_hotels(self):
        """test api point hotels status Ok and template"""
        response = requests.head(url=self.api_url_hotels, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))        
        self.assertEqual(response.status_code, 200)
        

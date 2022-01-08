from django.test import TestCase
from django.urls import reverse,resolve
from city.views import CityListView,get_city_hotels,get_city_hotels_search

class TestUrls(TestCase):
    
    def test_all_cities(self):
        url = reverse('city:all-cities')
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func.view_class,CityListView)

    def test_dj_ajax_select_request_search(self):
        url = reverse('city:city-hotels-search')
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func,get_city_hotels_search)

    def test_ajax_request_via_a_tag(self):
        url = reverse('city:city-hotels',kwargs={'city_name':'zoo'})
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func,get_city_hotels)

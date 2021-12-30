from django.test import TestCase
from django.urls import reverse,resolve
from city.views import CityListView,get_city_hotels,get_city_hotels_search

# ResolverMatch(func=city.views.view, args=(), kwargs={}, url_name='all-cities', app_names=['city'], namespaces=['city'], route='cities/show-all-cities/')


class TestUrls(TestCase):
    
    def test_all_cities(self):
        url = reverse('city:all-cities')
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func.view_class,CityListView)

    def test_ajax_request_search(self):
        url = reverse('city:city-hotels-search')
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func,get_city_hotels_search)

    def test_ajax_request_a_tagc(self):
        url = reverse('city:city-hotels',args=['city-slug'])
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func,get_city_hotels)

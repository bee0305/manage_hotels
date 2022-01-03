from django.test import TestCase, Client
from django.urls import reverse
from city.models import Hotel, City


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.all_cities_url = reverse('city:all-cities')
        self.ajax_url = reverse('city:city-hotels', kwargs={'city_name': 'zoo'})
        self.ajax_search_url = reverse('city:city-hotels-search')
        self.city = City.objects.create(name='zoo', short_cut='abc')
        self.hotel = Hotel.objects.create(name='qwerty', short_cut='try', unid='uiop', city=self.city)

    def test_get_ajax(self):
        response = self.client.get(self.ajax_url)
        expected_content = {'hotels': '[{"name": "qwerty", "id": 1}]', 'city': '{"city": "zoo"}'}
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_content
        )

    def test_list_cities_search_form_jquery(self):
        """
        check if context contains a form with city== field obj class AutoCompleteSelectField (jquery)
        """
        resp = self.client.get(self.all_cities_url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['search_city_form'].is_bound, False)
        self.assertEqual(
            resp.context['search_city_form'].fields['city'].__class__.__name__, 'AutoCompleteSelectField')
        self.assertTemplateUsed(resp, 'cities/show_cities.html')

    def test_get_ajax_search(self):
        """
        test search_city_form with city == integer(id=city) jquery module disign
        example get request: GET /cities/city-hotels-search/?city_text=&city=6 HTTP/1.1
        
        """
        data = {'city': 1}
        resp = self.client.get(self.ajax_search_url, data)
        json_resp_content = self.client.get(self.ajax_search_url, data).json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_resp_content.get('hotels'), [{'name': 'qwerty', 'id': 1}])
        self.assertEqual(len(json_resp_content.get('hotels')), 1)

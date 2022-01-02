import requests
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from requests.auth import HTTPBasicAuth
from django.utils import timezone
from utils.request_help import make_request_cities, make_request_hotels_slow


class Command(BaseCommand):
    """
        two blocks: to fetch data from city api and hotel api with command:
        for cities:  $python manage.py  get_cities (or python manage.py  get_cities --fetch city)
        for hotels:  $python manage.py  get_cities --fetch hotel
        First request.head if resp OK => request.get         
    """  
    help = 'Make api call to fetch all cities or hotels'  
    def add_arguments(self,parser):
        parser.add_argument('--fetch',default='city')  

    def handle(self, *args, **options):    
         
        time = timezone.now().strftime('%X') # 15:33:07
        if options['fetch'] =='city':
            url = settings.CITY_URL
            try:
                resp = requests.head(url=url,auth=HTTPBasicAuth(settings.CSV_HOST,settings.CSV_PSW))
                if resp.status_code == 200:                    
                    make_request_cities(url)  
                    self.stdout.write(self.style.SUCCESS(f"Last request at:{time} city api; code {resp.status_code}"))
                    print('end request cities')
                    # TODO: logging
                else:
                    # TODO: logging
                    self.stdout.write(self.style.ERROR(f"Failed request cities  at:{time} code: {resp.status_code}"))
            except Exception as e:                
                self.stdout.write(self.style.ERROR(f"Api city server responded at: {time} with status code== {resp.status_code}"))
                self.stdout.write(self.style.ERROR(f"Api city server error: {e}"))
                # TODO: logging

        elif options['fetch'] == 'hotel':            
            url = settings.HOTEL_URL
            print('api call to fetch hotels')
            try:
                resp = requests.head(url=url,auth=HTTPBasicAuth(settings.CSV_HOST,settings.CSV_PSW))         
                if resp.status_code == 200:
                    make_request_hotels_slow(url)
                    self.stdout.write(self.style.SUCCESS(f"Last request at:{time} hotel api; code 200"))
                else:
                    # TODO: logging
                    self.stdout.write(self.style.ERROR(f"Failed request hotels at:{time} code: {resp.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Api hotel server responded at: {time} with status code== {resp.status_code}"))
                # TODO: logging



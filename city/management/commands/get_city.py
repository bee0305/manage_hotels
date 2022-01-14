import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from utils.request_help import make_request_cities


class Command(BaseCommand):
    """        
        for cities:  $python manage.py  get_cities (or python manage.py  get_cities --fetch city)
        If request.head if resp OK => start request.get   to fetch data      
    """
    help = 'Make api call to fetch all cities'

    def handle(self, *args, **options):

        time = timezone.now().strftime('%X')  # 15:33:07        
        url = settings.CITY_URL
        try:
            resp = requests.head(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
            if resp.status_code == 200:               
                make_request_cities(url)                
                self.stdout.write(self.style.SUCCESS(f"Last request at:{time} city api; code {resp.status_code}"))
                print('end request cities; OK')
                # TODO: logging
                # temp for testing to log info
                with open('./city_info.txt','a') as fh:
                    fh.write(f'api call OK at: {time}')
            else:
                # TODO: logging
                self.stdout.write(self.style.ERROR(f"Failed request cities  at:{time} code: {resp.status_code}"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Api city server responded at: {time} with status code== {resp.status_code}"))
            self.stdout.write(self.style.ERROR(f"Api city server error: {e}"))
            # TODO: logging
            # temp for testing to log
            with open('./city_info.txt','a') as fh:
                    fh.write(f'api call failed at: {time}')

        
        
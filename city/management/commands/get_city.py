import requests
import logging
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from utils.request_help import make_request_cities

logger = logging.getLogger('django')

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
                logger.info(f'OK status: 200') 
                
            else:
                logger.warning(f'Failed request at {timezone.now()} status: {resp.status_code}') 
                self.stdout.write(self.style.ERROR(f"Failed request cities  at:{time} code: {resp.status_code}"))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed requ api city; server responded at: {time} with status code== {resp.status_code}"))
            self.stdout.write(self.style.ERROR(f"Api city server error: {e}"))           
            logger.warning(f'At {timezone.now()} status: {e}') 
            
            

        
        
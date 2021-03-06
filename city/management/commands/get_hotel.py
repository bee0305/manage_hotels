import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from utils.request_help import make_request_hotels_slow


class Command(BaseCommand):
    """
        for hotels:  $python manage.py  get_hotel
        If request.head if resp OK => start request.get to fetch hotel data    
    """
    help = 'Make api call to fetch all cities or hotels'

    def handle(self, *args, **options):

        time = timezone.now().strftime('%X')  # 15:33:07        
        url = settings.HOTEL_URL
        print('api call to fetch hotels')
        try:
            resp = requests.head(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
            if resp.status_code == 200:
                make_request_hotels_slow(url)
                self.stdout.write(self.style.SUCCESS(f"Last request at:{time} hotel api; code 200"))
            else:
                # TODO: logging
                self.stdout.write(self.style.ERROR(f"Failed request hotels at:{time} code: {resp.status_code}"))
                # temp for testing
                with open('./hotel_info.txt','w') as fh:
                    fh.write(f'api call OK at: {time}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Api hotel server responded at: {time} with status code== {resp.status_code}"))
            # TODO: logging
            with open('./hotel_info.txt','w') as fh:
                    fh.write(f'api call failed at: {time}')

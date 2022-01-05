import requests
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from requests.auth import HTTPBasicAuth
from django.utils import timezone
from utils.request_help import write_to_csv


class Command(BaseCommand):
    """
        two blocks: to 'catch' data from city api and hotel api with command
        AND write info to csv files:
        for cities:  $python manage.py  get_cities (or python manage.py  get_cities --catch city)
        for hotels:  $python manage.py  get_cities --catch hotel
        First request.head if resp OK => request.get         
    """
    help = 'Make api call to fetch all cities or hotels'

    def add_arguments(self, parser):
        parser.add_argument('--catch', default='city')

    def handle(self, *args, **options):

        time = timezone.now().strftime('%X')  # 15:33:07
        if options['catch'] == 'city':
            url = settings.CITY_URL
            try:
                resp = requests.head(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
                # TODO: log
                if resp.status_code == 200:
                    print('url', url)
                    resp = requests.get(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
                    print(resp.content)
                    write_to_csv(resp.content,'csv_src/city.csv')
                    print('done')
                    self.stdout.write(self.style.SUCCESS(f"Last request at:{time} city api; code {resp.status_code}"))
                    print('end request cities')
                    # TODO: logging
                else:
                    # TODO: logging
                    self.stdout.write(self.style.ERROR(f"Failed request cities  at:{time} code: {resp.status_code}"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Api city server responded at: {time} with status code== {resp.status_code}"))
                self.stdout.write(self.style.ERROR(f"Api city server error: {e}"))
                # TODO: logging

        elif options['catch'] == 'hotel':
            url = settings.HOTEL_URL            
            try:
                resp = requests.head(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
                # TODO: log
                if resp.status_code == 200:
                    resp = requests.get(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
                    resp = requests.get(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
                    write_to_csv(resp.content,'csv_src/hotel.csv')
                    print('done')
                    self.stdout.write(self.style.SUCCESS(f"Last request at:{time} hotel api; code 200"))
                else:
                    # TODO: logging
                    self.stdout.write(self.style.ERROR(f"Failed request hotels at:{time} code: {resp.status_code}"))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Api hotel server responded at: {time} with status code== {resp.status_code}"))
                # TODO: logging

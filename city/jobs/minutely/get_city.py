from django_extensions.management.jobs import MinutelyJob
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

from django.utils import timezone
from utils.request_help import make_request_cities


class Job(MinutelyJob):
    """
        two blocks: to fetch data from city api and hotel api with command:
        for cities:  $python manage.py  get_cities (or python manage.py  get_cities --fetch city)
        for hotels:  $python manage.py  get_cities --fetch hotel
        First request.head if resp OK => request.get         
    """
    help = 'Make api call to fetch all cities or hotels'

    def execute(self):
        time = timezone.now().strftime('%X')  # 15:33:07        
        url = settings.CITY_URL
        try:
            resp = requests.head(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
            if resp.status_code == 200:               
                # make_request_cities(url)                
                # self.stdout.write(self.style.SUCCESS(f"Last request at:{time} city api; code {resp.status_code}"))
                print('end request cities; OK')
                # TODO: logging
                # temp for testing to log info
                with open('./rio.txt','a') as fh:
                    fh.write(f'api call OK at: {time}')
            else:
                print('status !=200')
        except Exception as e:
            # self.stdout.write(
                # self.style.ERROR(f"Api city server responded at: {time} with status code== {resp.status_code}"))
            # self.stdout.write(self.style.ERROR(f"Api city server error: {e}"))
            # TODO: logging
            # temp for testing to log
            with open('./rio.txt','a') as fh:
                    fh.write(f'api call failed at: {time}')



       
# class Job(BaseJob):
#     help = "Test from hourly dir."

#     def execute(self):
#         # executing empty sample job
#         print("greet from smaple2.py hourly")
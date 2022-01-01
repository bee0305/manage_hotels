import requests
from requests.auth import HTTPBasicAuth
import csv
import timeit

from django.core.exceptions import RequestAborted
from django.conf import settings

from city.models import City
from .utils import ApiCustomException
# from .utils import file_generator_csv #local csv files; see Option N2 below



# Option N1
# delete existing data
# fetch data fron api point and create city objects

def run(): 
    # name is essential for django-extensions module; can't be changed for another!  
    start = timeit.default_timer()   
    City.objects.delete()  
    resp = requests.get(url=settings.HOTEL_URL,auth=HTTPBasicAuth(settings.CSV_HOST,settings.CSV_PSW))    
    # splitting on \n chars; returns iterable for csv.reader method
    lines = resp.text.splitlines()
    reader = csv.reader(lines)
    temp = [] 
    try:      
        for row in reader:
            collection = row[0].split(';')
            if collection:
                short_cut  = str(collection[0])
                name = collection[1].strip('"')            
                city = City(name=name,short_cut=short_cut)
                temp.append(city)
                      
            else:
                continue
        City.objects.bulk_create(temp)    
        finish = timeit.default_timer()            
        print('Total time for this code is',finish - start)    
    except RequestAborted:
        print('request not success') 
        # TODO: add logger here   
    except ApiCustomException:
        print('smth went wrong with api call') 
        # TODO: add logger here           
    


# Option N2: 
# delete existing city objects in db
# read from local csv file and create city objects

# def run():   
#     # all_cities = City.objects.delete()     
#     file_generator = file_generator_csv('csv_src/city.csv')
#     for row in file_generator:
#         collection = row[0].split(';')
#         if collection:
#             short_cut  = str(collection[0])
#             name = collection[1].strip('"')            
#             city,_= City.objects.get_or_create(name=name,short_cut=short_cut)
#             # TODO: add logger here         
#         else:
#             continue 
        

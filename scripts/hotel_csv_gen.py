import requests
from requests.auth import HTTPBasicAuth
import csv
import timeit

from django.shortcuts import get_object_or_404
from django.conf import settings

from city.models import Hotel,City
#from .utils import file_generator_csv    # local csv file see below (option N2)


# Option N1
# delete existing hotel objects
# fetch data fron api point abd create new hotel objects

def run(): 
    # name is essential for django-extensions module; can't be changed for another!
    start = timeit.default_timer()   
    Hotel.objects.all().delete()  
    resp = requests.get(url=settings.HOTEL_URL,auth=HTTPBasicAuth(settings.CSV_HOST,settings.CSV_PSW))    
    # splitting on \n chars; returns iterable for csv.reader method
    lines = resp.text.splitlines()
    reader = csv.reader(lines)
    temp = []       
    for row in reader:        
        collection = row[0].split(';')
        if collection:    
            short_cut  = str(collection[0].strip('"'))
            unid  = str(collection[1].strip('"'))
            name = collection[2].strip('"')
            city = get_object_or_404(City,short_cut=short_cut)
            hotel = Hotel(unid=unid,short_cut = short_cut,name=name,city=city)  
            temp.append(hotel)
            # TODO: add logger here    
            
        else:
            continue 
    Hotel.objects.bulk_create(temp,batch_size=200)     
    finish = timeit.default_timer()            
    print('Total time for this code is',finish - start)
    # via api point =  0.4508142999984557 sec 


# Option N2 (work with downloaded csv files )    
# def run(): 
#     start = timeit.default_timer()   
#     Hotel.objects.all().delete()  
#     temp = []   
#     file_generator = file_generator_csv('csv_src/hotel.csv')
#     for row in file_generator:        
#         collection = row[0].split(';')
#         if collection:    
#             short_cut  = str(collection[0].strip('"'))
#             unid  = str(collection[1].strip('"'))
#             name = collection[2].strip('"')
#             city = get_object_or_404(City,short_cut=short_cut)
#             hotel = Hotel(unid=unid,short_cut = short_cut,name=name,city=city)  
#             temp.append(hotel)
#             # TODO: add logger here    
            
#         else:
#             continue 
#     Hotel.objects.bulk_create(temp,batch_size=200)     
#     finish = timeit.default_timer()            
#     print('Total time for this code is',finish - start) 
    #via local csv file
    # delta without bulk_create == 33.03058509999937
    # delta with bulk_create    == 0.23692409999966912    
    # in case of update existed data |=> time delta ==  0.20917701721191406   
        


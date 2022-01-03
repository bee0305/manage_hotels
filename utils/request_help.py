import requests
import csv
from requests.auth import HTTPBasicAuth
from django.shortcuts import get_object_or_404
from django.conf import settings
from city.models import City, Hotel


def make_request_cities(url):
    resp = requests.get(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
    # splitting on \n chars; returns iterable for csv.reader method
    lines = resp.text.splitlines()
    reader = csv.reader(lines)
    for row in reader:
        #  row == list[one_string] ==['AMS;"Amsterdam"']
        collection = row[0].split(';')
        if collection:
            # "BER";"Berlijn"
            # print(collection[0],type(collection[0]))
            short_cut = str(collection[0])
            name = collection[1].strip('"')
            city, _ = City.objects.get_or_create(name=name, short_cut=short_cut)
            # TODO: add logger here         
        else:
            continue


def make_request_hotels_slow(url):
    """
    1.This func is slow but in case if api point requested on regular base and 
    hotel data already exists |=> method get_or_create more suitable for updating the data
    if changed on api ( can be improved with async task celery/raw sql if no need data validation)
    2.otherwise see solution with bulk_create: more suitable if existed data can be 
    deleted/overriden (see below func make_request_hotels_fast_with_bulk)       
    """
    resp = requests.get(url=url, auth=HTTPBasicAuth(settings.CSV_HOST, settings.CSV_PSW))
    # splitting on \n chars; returns iterable for csv.reader method
    lines = resp.text.splitlines()
    reader = csv.reader(lines)
    for row in reader:
        collection = row[0].split(';')
        if collection:
            short_cut = str(collection[0].strip('"'))
            unid = str(collection[1].strip('"'))
            name = collection[2].strip('"')
            city = get_object_or_404(City, short_cut=short_cut)
            hotel, _ = Hotel.objects.get_or_create(unid=unid, short_cut=short_cut, name=name, city=city)
            # TODO: add logger here    

        else:
            continue

# def make_request_hotels_fast_with_bulk(url):#
#     # used bulk_create for db 
#     temp = []        
#     resp = requests.get(url=url,auth=HTTPBasicAuth(...))
#     lines = resp.text.splitlines()
#     reader = csv.reader(lines)
#     for row in reader:
#         collection = row[0].split(';')
#         if collection:    
#             short_cut  = str(collection[0].strip('"'))
#             unid  = str(collection[1].strip('"'))
#             name = collection[2].strip('"')
#             city = get_object_or_404(City,short_cut=short_cut)
#             hotel = Hotel(unid=unid,short_cut = short_cut,name=name,city=city)   
#             temp.append(hotel)         
#             # TODO: logger here
#         else:
#             continue   
#     Hotel.objects.bulk_create(temp,batch_size=200)

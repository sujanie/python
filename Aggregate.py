#!/usr/bin/env python
import hotels
import tripadvisor
import booking

import requests
from bs4 import BeautifulSoup

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import xml.etree.cElementTree as ET
import sys
import warnings
from datetime import datetime
from time import time
import json


      

def aggregate(datalist):
    dict3=booking.parse(datalist[6])
    #print(len(data[1].content))
    dict1=hotels.get(datalist[0:6])
    warnings.filterwarnings("ignore")  
    dict2=tripadvisor.parse(datalist[7])
    
    
    hotel_data=[]
    hotel_list=[]
    output={}
    
    for hotel in dict3:
            hotel_list.append(hotel['Name'])
    #print hotel_list
    for item in dict1:
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        data={}
        
        # compare each hotel name irrespective of the position of the word in the hotel name
        for hotel in dict2:
            
            #print hotel['hotel_name'],x['Name']
            val=fuzz.token_sort_ratio(hotel['hotel_name'],item['Name'])
            if val>75:
                x=process.extractOne(hotel['hotel_name'],hotel_list)
                y=fuzz.token_sort_ratio(x[0],hotel['hotel_name'])
                if y>75:
                    list1.append(hotel['hotel_name'])
                    list2.append(val)
                    list3.append(hotel)
                    list4.append(x)
       
        if len(list2)!=0 and len(list4)!=0:
            maxi=list2.index(max(list2))
            if list4[maxi][1]>75:
                maxi2=hotel_list.index(list4[maxi][0])
                element=list3[maxi]
                element2=dict3[maxi2]
                data={
                        "Name":item['Name'],
                        "Address":item['address'],
                        "Features":element['hotel_features'],
                        "Rating_from_hotels":item['rate'],
                        "Price_from_hotels":item['price'],
                        "Url_of_hotels":item['url'],
                        "Image":item['image'],
                        "Rating_from_tripadvisor":element['tripadvisor_rating'],
                        "Price_from_tripadvisor":element['price_per_night'],
                        "Reviews":element['reviews'],
                        "booking_provider":element['booking_provider'],
                        "Url_of_tripadvisor":element['url'],
                        "Rating_from_booking":element2['rate'],
                        "Price_from_booking":element2['price'],
                        "Url_of_booking":element2['url'],
                        "Name##":element2['Name']
                    }
        if data!={}:
            hotel_data.append(data)
            
            print (data["Name##"],data["Name"],data["Price_from_hotels"],data["Price_from_tripadvisor"],data["Price_from_booking"])
    
    return json.dumps(hotel_data)


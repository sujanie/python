#!/usr/bin/env python
from datetime import datetime
from time import time
from lxml import html,etree
import requests,re
import os,sys


def parse(page):
    
    api_response  = page.json()
    #getting the TA url for the query from the autocomplete response
    
    url_from_autocomplete = "http://www.tripadvisor.com"+api_response['results'][0]['url']+str(50)
    #print 'URL found %s'%url_from_autocomplete
    geo = api_response['results'][0]['value']   
    
    #form data to get the hotels list from TA for the selected date
    form_data = {'changeSet': 'TRAVEL_INFO',
            'showSnippets': 'false',
            'staydates':'2019_06_07_2019_06_08',
            'uguests': '2',
            'sortOrder':'Popularity',
            'per_page':50
    }
    #Referrer is necessary to get the correct response from TA if not provided they will redirect to home page
    
    headers = {
                            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                            'Accept-Encoding': 'gzip,deflate',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                            'Host': 'www.tripadvisor.com',
                            'Pragma': 'no-cache',
                            'Referer': url_from_autocomplete,
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0',
                            'X-Requested-With': 'XMLHttpRequest'
                        }
    cookies=  {"SetCurrency":"USD"}
    
    page_response  = requests.post(url = url_from_autocomplete,data=form_data,headers = headers, cookies = cookies, verify=False)
    # change whole html file to a nice tree structure
    parser = html.fromstring(page_response.text)
    #This will create a list of hotels' details
    hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[contains(@class,"listing collapsed")]')
    hotel_data = []
    if not hotel_lists:
        hotel_lists = parser.xpath('//div[contains(@class,"listItem")]//div[@class="listing "]')
    #print "tripadvisor----"
    for hotel in hotel_lists:
        # construct xpath query for each hotel data
        XPATH_HOTEL_PRICE = './/div[contains(@data-sizegroup,"mini-meta-price")]//text()'
        XPATH_HOTEL_LINK = './/a[contains(@class,"property_title")]/@href'
        XPATH_REVIEWS  = './/a[@class="review_count"]//text()'
        XPATH_RANK = './/div[@class="popRanking"]//text()'
        XPATH_RATING = './/a[contains(@class,"ui_bubble_rating")]/@alt'
        XPATH_HOTEL_NAME = './/a[contains(@class,"property_title")]//text()'
        XPATH_HOTEL_FEATURES = './/div[contains(@class,"common_hotel_icons_list")]//li//text()'
        
        XPATH_BOOKING_PROVIDER = './/div[contains(@data-sizegroup,"mini-meta-provider")]//text()'

        raw_booking_provider = hotel.xpath(XPATH_BOOKING_PROVIDER)
        raw_hotel_price_per_night  = hotel.xpath(XPATH_HOTEL_PRICE)
        raw_hotel_link = hotel.xpath(XPATH_HOTEL_LINK)
        raw_no_of_reviews = hotel.xpath(XPATH_REVIEWS)
        raw_rank = hotel.xpath(XPATH_RANK)
        raw_rating = hotel.xpath(XPATH_RATING)
        raw_hotel_name = hotel.xpath(XPATH_HOTEL_NAME)
        raw_hotel_features = hotel.xpath(XPATH_HOTEL_FEATURES)
        # change format of the data
        price_per_night = ''.join(raw_hotel_price_per_night).replace('\n','') if raw_hotel_price_per_night else None
        url = 'http://www.tripadvisor.com'+raw_hotel_link[0] if raw_hotel_link else  None
        reviews = ''.join(raw_no_of_reviews).replace("reviews","").replace(",","") if raw_no_of_reviews else 0 
        rank = ''.join(raw_rank) if raw_rank else None
        rating = ''.join(raw_rating).replace('of 5 bubbles','').strip() if raw_rating else None
        name = ''.join(raw_hotel_name).strip() if raw_hotel_name else None
        hotel_features = ','.join(raw_hotel_features)
        booking_provider = ''.join(raw_booking_provider).strip() if raw_booking_provider else None

        
            
        data = {
                    'hotel_name':name,
                    'url':url,
                    'reviews':reviews,
                    'tripadvisor_rating':rating,
                    'hotel_features':hotel_features,
                    'price_per_night':price_per_night,
                    'booking_provider':booking_provider

        }
        hotel_data.append(data)
        #print data['price_per_night'],data['hotel_features']
        
        print (data['price_per_night'])
    print (len(hotel_data))
    return hotel_data


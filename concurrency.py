import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import urllib.request
import requests
import threading
from time import time
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os,sys

datalist=[]
URLS=[]
thread_local = threading.local()


def construct_url(city,checkin,checkout,num):
   checkin_date=datetime.strptime(checkin, "%m/%d/%Y")
   checkout_date=datetime.strptime(checkout, "%m/%d/%Y")
   #change date format
   #print checkin_date
   checkIn = checkin_date.strftime("%Y-%m-%d")
   checkOut = checkout_date.strftime("%Y-%m-%d")
   #format hotel urls
   for i in range(6):
      url1="https://www.hotels.com/search.do?q-check-in="+checkIn+"&q-room-0-adults=1&q-destination="+city+"&per_page=50&q-rooms="+str(num)+"&q-check-out="+checkOut+"&q-room-0-children=0&pn="+str(i)
      URLS.append(url1)

   url="https://www.booking.com/searchresults.en-gb.html?ss="+city+"&checkin_year_month_monthday="+checkIn+"&checkout_year_month_monthday="+checkOut+"&group_adults=2&group_children=0&no_rooms=1&rows=50&selected_currency=USD&changed_currency=1&top_currency=1&nflt="
   
   geo_url = 'https://www.tripadvisor.com/TypeAheadJson?action=API&startTime='+str(int(time()))+'&uiOrigin=GEOSCOPE&source=GEOSCOPE&interleaved=true&types=geo,theme_park&neighborhood_geos=true&link_type=hotel&details=true&max=12&injectNeighborhoods=true&query='+city+'50'
   
   URLS.append(url)
   URLS.append(geo_url)
   return URLS


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session
   

def load_url(url):
   headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

   session = get_session()
   retry = Retry(connect=30, backoff_factor=0.5)
   adapter = HTTPAdapter(max_retries=retry)
   session.mount('http://', adapter)
   session.mount('https://', adapter)
   with session.get(url,headers=headers) as response:
      return response


   

def main(urls):
   
   print (urls)
   with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
      results = executor.map(load_url, urls)
      print (results)
      try:
         for result in results:
            datalist.append(result)
            #print(result)
      except Exception as exc:
           print(' generated an exception: %s' % ( exc))   
   return datalist

 

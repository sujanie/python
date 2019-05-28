import requests
from bs4 import BeautifulSoup

from lxml import html,etree
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime
import time
name=[]
price=[]
rate=[]
urllist=[]
review=[]
hotel_data=[]

def parse(page):
    #parsed into beautifulsoup
    parsed_html = BeautifulSoup(page.content, 'lxml')
    item=parsed_html.find(class_='hotellist_wrap tracked shorten_property_block')
    
    hotel_list = item.find_all('div',class_="sr_item sr_item_new sr_item_default sr_property_block sr_item_bs sr_flex_layout")
    hotel_list.extend(item.find_all('div',class_="sr_item sr_item_new sr_item_default sr_property_block sr_flex_layout"))
    # get data using html elements
    for i in hotel_list:
        name.append(i.find('span',class_="sr-hotel__name").get_text().strip('\n'))
        #review.append(i.find('div',class_="bui-review-score__text").get_text().strip('\n'))
        val=i.find('div',class_='price scarcity_color')
        val1=i.find('div',class_='bui-price-display__value prco-inline-block-maker-helper')
        val2=i.find('b',class_="sr_gs_price_total")
        val3=i.find('strong',class_="price availprice no_rack_rate")
        val4=i.find('strong',class_="price scarcity_color")
        val5=i.find('div',class_="totalPrice totalPrice_no-rack-rate entire_row_clickable")
           
        if val!=None:
            price.append(val.get_text().strip())
        elif val!=None:
            price.append(val1.get_text().strip())
        elif val2!=None:
            price.append(val2.get_text().strip())
        elif val3!=None:
            price.append(val3.get_text().strip())
        elif val4!=None:
            price.append(val4.get_text().strip())
        elif val5!=None:
            price.append(val5.get_text().strip())
        else:
            price.append(0)
        # get rating data
        rating=i.find('div',class_='bui-review-score__badge')
        if rating==None:
            rating=i.find('span',class_='review-score-badge')
            
        if rating!=None:
             
            rates=float(rating.get_text().strip())
        else:
            rates=0.0
        # format rating
        rate.append(round(rates)/2)
        # get hotel url
        hotelurl=i.find('a',class_="hotel_name_link url").get('href').strip()
        urllist.append('https://www.booking.com/'+str(hotelurl))
    print (len(price),len(rate),len(urllist))
    
    # format data into the dictionary
    for i in range(len(hotel_list)):
        data={}
        data['Name']=name[i]
        data['rate']=rate[i]
        data['url']=urllist[i]
        data['price']=price[i]
        hotel_data.append(data)
        #print name[i]
    #print"====================="
                    
    return hotel_data 
#parse('Chennai','06/18/2019','06/19/2019')

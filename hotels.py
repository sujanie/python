#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

from lxml import html,etree

from datetime import datetime
import time

def get(page):
        localtime = time.localtime(time.time())
        #print localtime
        #change as date obj
        #checkin_date=datetime.strptime(checkin_date, "%m/%d/%Y")
        #checkout_date=datetime.strptime(checkout_date, "%m/%d/%Y")
        #change date format
        #print checkin_date
        #checkIn = checkin_date.strftime("%Y-%m-%d")
        #checkOut = checkout_date.strftime("%Y-%m-%d")
        hotel_listitem=[]
        hotel_urllist=[]
        hotel_price=[]
        hotel_rate=[]
        hotel_image=[]
        hotel_address=[]
        data={}
        output=[]
        for i in range(6):
                name=[]
                url=[]
                rate=[]
                price=[]
                image=[]
                contactlist=[]
                soup = BeautifulSoup(page[i].content, 'lxml')
                #print(type(page.content),len(soup))
               
                item = soup.find(class_="h-listing")
                localtime = time.localtime(time.time())
                
                #delete unavailable hotel data which are sold out
                [x.extract() for x in item.findAll(class_='hotel sold-out')]
                [x.extract() for x in item.findAll(class_='hotel sold-out-flag sold-out')]
                [x.extract() for x in item.findAll(class_='hotel sponsored sold-out')]
                [x.extract() for x in item.findAll(class_='hotel sold-out-flag vip sold-out')]    
                [y.extract() for y in item.findAll(class_='hotel sold-out pinned-unavailable check-availability-overlay')]
                # select div element as i want to display
                #print item.prettify()
                localtime = time.localtime(time.time())
                #print localtime
                hotel_list = item.select(".hotel-wrap .p-name")
                rating=item.select(".hotel-wrap .star-rating-text")
                rating1=item.select(".hotel-wrap .star-rating-text star-rating-text-strong")
                pricelist=item.select(".hotel-wrap .price ")
                contactlist=item.select(".hotel-wrap .contact")
                contactlist1=item.select(".hotel-wrap .property-landmarks")
                imagelist=item.select(".hotel-wrap .property-image-link")
                
                if len(contactlist)==0:
                        contactlist=contactlist1
                        
                urllist=item.select(".hotel-wrap .cta")
                rating.extend(rating1)
                # get hotel name
                name = [pt.get_text().lstrip('u') for pt in hotel_list]
                # get hotel rate
                rate= [x.get_text() for x in rating]
                
                
                # get price data
                for item in pricelist:
                        x=item.select('ins')
                        x1=item.select('strong')
                        x2=item.select('.current-price has-old-price bold')
                        for z in x:
                                price.append(z.get_text())
                        for z1 in x1:
                                price.append(z1.get_text())
                        for z2 in x2:
                                price.append(z2.get_text())
                # get image
                for item in imagelist:
                        
                        x=item.find(class_="u-photo use-bgimage featured-img-tablet")
                        if x==None:
                                x=item.find(class_="u-photo use-bgimage image-loader featured-img-tablet")
                        
                        y=x.get('style')
                        image.append(y.replace("background-image:url('",'').rstrip("')"))
                 
                        
                # get contact data
                contact= [z.get_text() for z in contactlist]
                      
                hotel_url=[]
                # get url data
                for url in urllist:
                        
                        x=(str(url).split('"/',1))[1].split('target="_')
                        
                        z=(x[0].replace('"','')).replace('amp;','')
                        
                        string="https://www.hotels.com/"
                        hotel_url.append(string+z)
                # append all data into the corresponded files
                hotel_listitem.extend(name)
                hotel_urllist.extend(hotel_url)
                hotel_price.extend(price)
                hotel_rate.extend(rate)
                hotel_address.extend(contact)
                hotel_image.extend(image)
                
        
        # get unique hotel details             
        print (len(hotel_rate),len(hotel_listitem),len(hotel_address),len(hotel_price),len(hotel_image))
        
        for i in range(len(hotel_listitem)):
                data={}
                if (hotel_listitem.count(hotel_listitem[i])!=1)& (hotel_listitem[i]!="#"):
                        for n, j in enumerate(hotel_listitem):
                                
                                if j == hotel_listitem[i]:
                                        hotel_listitem[n]='#'
                if(hotel_listitem[i]!="#"):
                        print (hotel_listitem[i])
                        data['price']=hotel_price[i]
                        data['url']=hotel_urllist[i]
                        data['rate']=hotel_rate[i]
                        data['address']=hotel_address[i]
                        data['image']=hotel_image[i]
                        data['Name']=hotel_listitem[i]
                        
                if data!={}:       
                        output.append(data)
        
        return output

import requests
from bs4 import BeautifulSoup
import unittest

class Test(unittest.TestCase):
   bs = None
   def setUp(self):
      url = "https://www.hotels.com/search.do?q-check-in=2019-05-07&q-room-0-adults=1&q-destination=Colombo&per_page=50&pn=0&q-rooms=1&q-check-out=2019-05-08&q-room-0-children=0"
      url1= "http://www.tripadvisor.com/Hotels-g293962-Colombo_Western_Province-Hotels.html50"
      page=requests.get(url)
      Test.bs = BeautifulSoup(page.content, 'html.parser')
      page1=requests.get(url1)
      Test.bs1 = BeautifulSoup(page1.content, 'html.parser')
      
   def test_titleText(self):
      pageTitle = Test.bs.find('title').get_text()
      self.assertEqual('Hotels.com - hotels in Colombo, Sri Lanka', pageTitle);
      pageTitle1 = Test.bs1.find('title').get_text()
      self.assertEqual('THE 10 BEST Hotels in Colombo for 2019 (from $14) - TripAdvisor', pageTitle1);
      
   def test_contentExists(self):
      content = Test.bs.find('div',{'id':'listings'})
      self.assertIsNotNone(content)
      content1 = Test.bs1.find('div',{'id':'MAINWRAP'})
      self.assertIsNotNone(content1)
if __name__ == '__main__':
   unittest.main()
   
   

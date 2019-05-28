#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
import Aggregate
import concurrency
import sys
PORT_NUMBER = 8080
from urllib.parse import parse_qs
#This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):
        #Handler for the GET requests
        def do_GET(self):
                path, _, query_string = self.path.partition('?')
                queryData = parse_qs(query_string)
                city = queryData.get("city")[0]
                checkIn = queryData.get("checkIn")[0]
                checkOut = queryData.get("checkOut")[0]
                num = queryData.get("num")[0]
                num1 = queryData.get("num1")[0]

                print (city)
                print (checkIn)
                print (checkOut)
                print (num)
                print (num1)

                URLS=concurrency.construct_url(city,checkIn,checkOut,num)
                if __name__ == '__main__':
                        details=concurrency.main(URLS)
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.end_headers()
                        data=Aggregate.aggregate(details)
                        # Send the html message
                        
                        data=str.encode(data)
                        
                        self.wfile.write(data)


def run():
        try:
                #Create a web server and define the handler to manage the
                #incoming request
                server = HTTPServer(('127.0.0.1', PORT_NUMBER), myHandler)
                print ("Started httpserver on port " , PORT_NUMBER)
                #Wait forever for incoming htto requests
                server.serve_forever()

        except KeyboardInterrupt:
                print ("^C received, shutting down the web server")
                server.socket.close()
if __name__ == '__main__':

        from sys import argv

        run()

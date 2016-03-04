#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import urllib
import urllib2
import string
import threading
import time

global select_mode
global colorAuto
valuetest = 0

def sendColor(red, green, blue):
    url_send = 'http://10.13.9.37/arduino/color/' + str(red) + '/' + str(green) + '/' + str(blue)
    #print url_send
    urllib2.urlopen(url_send)
    #time.sleep(0.001) # 1ms

def rainbow():
    global valuetest
    while(valuetest):
        print("Thread started!")
        red = 255
        green = 0
        blue = 0
        for i in range(0, 255):
            blue += 1
            sendColor(red, green, blue)
        for i in range(0, 255):
            red -= 1
            sendColor(red, green, blue)
        for i in range(0, 255):
            green += 1
            sendColor(red, green, blue)
        for i in range(0, 255):
            blue -= 1
            sendColor(red, green, blue)
        for i in range(0, 255):
            red += 1
            sendColor(red, green, blue)
        for i in range(0, 255):
            green -= 1
            sendColor(red, green, blue)

class GetHandler(BaseHTTPRequestHandler):
    def select_MODE(self):
        global valuetest
        select_mode = 0
        color_auto = 0
        parsed_path = urlparse.urlparse(self.path)
        choice = self.path
        cleaned = choice.split("/")

        if cleaned[1] == 'auto' and cleaned[2] == '1' :
            colorAuto = threading.Thread(target=rainbow)
            valuetest = 1
            colorAuto.start()
            
        if cleaned[1] == 'auto' and cleaned[2] == '0' :
            valuetest = 0
            colorAuto._stop()
            print("Thread stopped!")
            
        if cleaned[1] == 'manual' :
            select_mode = 'color/' + cleaned[2] + '/' + cleaned[3] + '/' + cleaned[4]
            print "manual"

        return select_mode

    def do_GET(self):
        mode = self.select_MODE()
        
        if mode != 0:
            url = 'http://10.13.9.37/arduino/' + mode
            response = urllib2.urlopen(url).read()
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response)
        return

if __name__ == '__main__':

    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('10.13.9.53', 8080), GetHandler)
    print 'Starting LightAndChill server on 8080, use <Ctrl-C> to stop'
    server.serve_forever()

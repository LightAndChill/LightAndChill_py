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

def rainbow():
    print("Thread started!")
    #url = 'http://10.13.9.37/arduino/manual/100/0/0'
    #response = urllib2.urlopen(url).read()
            
    #self.send_response(200)
    #self.end_headers()
    #self.wfile.write(response)

class GetHandler(BaseHTTPRequestHandler):
    def select_MODE(self):
        select_mode = 0
        color_auto = 0
        parsed_path = urlparse.urlparse(self.path)
        choice = self.path
        cleaned = choice.split("/")

        if cleaned[1] == 'auto' and cleaned[2] == '1' :
            colorAuto = threading.Thread(target=rainbow)
            colorAuto.start()
            
        if cleaned[1] == 'auto' and cleaned[2] == '0' :
            colorAuto = threading.Thread(target=rainbow)
            colorAuto.stop()
            
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
    server = HTTPServer(('localhost', 8080), GetHandler)
    print 'Starting LightAndChill server on 8080, use <Ctrl-C> to stop'
    server.serve_forever()

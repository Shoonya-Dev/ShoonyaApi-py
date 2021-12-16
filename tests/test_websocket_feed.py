import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import datetime
import logging
import time
import yaml
import pandas as pd

#sample
logging.basicConfig(level=logging.DEBUG)

#flag to tell us if the websocket is open
socket_opened = False

#application callbacks
def event_handler_order_update(message):
    print("order event: " + str(message))


SYMBOLDICT = {}
def event_handler_quote_update(message):
    global SYMBOLDICT
    #e   Exchange
    #tk  Token
    #lp  LTP
    #pc  Percentage change
    #v   volume
    #o   Open price
    #h   High price
    #l   Low price
    #c   Close price
    #ap  Average trade price

    print("quote event: {0}".format(time.strftime('%d-%m-%Y %H:%M:%S')) + str(message))
    
    key = message['e'] + '|' + message['tk']

    if key in SYMBOLDICT:
        symbol_info =  SYMBOLDICT[key]
        symbol_info.update(message)
        SYMBOLDICT[key] = symbol_info
    else:
        SYMBOLDICT[key] = message

    print(SYMBOLDICT[key])

def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')
    
    api.subscribe('NSE|11630', feed_type='d')
    #api.subscribe(['NSE|22', 'BSE|522032'])

#end of callbacks

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)

#start of our program
api = ShoonyaApiPy()

#yaml for parameters
with open('..\\cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

if ret != None:   
    ret = api.start_websocket(order_update_callback=event_handler_order_update, subscribe_callback=event_handler_quote_update, socket_open_callback=open_callback)
    
    while True:
        if socket_opened == True:
            print('q => quit')
            prompt1=input('what shall we do? ').lower()    

            print('Fin') #an answer that wouldn't be yes or no
            break   

        else:
            continue

    
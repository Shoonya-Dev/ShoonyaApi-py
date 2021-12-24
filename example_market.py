from api_helper import ShoonyaApiPy, get_time
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


def event_handler_quote_update(message):
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
    

def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')
    
    api.subscribe('NSE|11630')
    #api.subscribe(['NSE|22', 'BSE|522032'])

#end of callbacks

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)

#start of our program
api = ShoonyaApiPy()

#use following if yaml isnt used
#user    = <uid>
#pwd     = <password>
#factor2 = <2nd factor>
#vc      = <vendor code>
#apikey  = <secret key>
#imei    = <imei>

#ret = api.login(userid = user, password = pwd, twoFA=factor2, vendor_code=vc, api_secret=apikey, imei=imei)

#yaml for parameters
with open('cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

if ret != None:   
    while True:
        print('f => find symbol')    
        print('m => get quotes')
        print('p => contract info n properties')    
        print('v => get 1 min market data')
        print('t => get today 1 min market data')
        print('d => get daily data')
        print('o => get option chain')
        print('s => start_websocket')
        print('q => quit')

        prompt1=input('what shall we do? ').lower()                    
        
        if prompt1 == 'v':
            start_time = "09-07-2021 00:00:00"
            end_time = time.time()
            
            start_secs = get_time(start_time)

            ret = api.get_time_price_series(exchange='NSE', token='22', starttime=start_secs, endtime=end_time)
            
            df = pd.DataFrame.from_dict(ret)
            print(df)            
            
        elif prompt1 == 't':
            ret = api.get_time_price_series(exchange='NFO', token='71321')
            
            df = pd.DataFrame.from_dict(ret)
            print(df)                        

        elif prompt1 == 'f':
            exch  = 'NFO'
            query = 'BANKNIFTY 30DEC CE 34'
            ret = api.searchscrip(exchange=exch, searchtext=query)
            print(ret)

            if ret != None:
                symbols = ret['values']
                for symbol in symbols:
                    print('{0} token is {1}'.format(symbol['tsym'], symbol['token']))

        elif prompt1 == 'd':
            exch  = 'NSE'
            tsym = 'RELIANCE-EQ'
            ret = api.get_daily_price_series(exchange=exch, tradingsymbol=tsym, startdate=0)
            print(ret)

        elif prompt1 == 'p':
            exch  = 'NSE'
            token = '22'
            ret = api.get_security_info(exchange=exch, token=token)
            print(ret)

        elif prompt1 == 'm':
            exch  = 'NSE'
            token = '22'
            ret = api.get_quotes(exchange=exch, token=token)
            print(ret)

        elif prompt1 == 'o':
            exch  = 'NFO'
            tsym = 'COFORGE30DEC21F'
            chain = api.get_option_chain(exchange=exch, tradingsymbol=tsym, strikeprice=3500, count=2)

            chainscrips = []
            for scrip in chain['values']:
                scripdata = api.get_quotes(exchange=scrip['exch'], token=scrip['token'])
                chainscrips.append(scripdata)

            print(chainscrips)

        elif prompt1 == 's':

            if socket_opened == True:
                print('websocket already opened')
                continue

            ret = api.start_websocket(order_update_callback=event_handler_order_update, subscribe_callback=event_handler_quote_update, socket_open_callback=open_callback)
            print(ret)

        else:
            ret = api.logout()
            print(ret)
            print('Fin') #an answer that wouldn't be yes or no
            break

    
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import signal
import datetime
import logging
import time
import yaml
import pandas as pd
import xlsxwriter
import xlwings as xw

#sample
logging.basicConfig(level=logging.DEBUG)

#flag to tell us if the websocket is open
socket_opened = False

#application callbacks
def event_handler_order_update(message):
    print("order event: " + str(message))


SYMBOLDICT = {}
def event_handler_quote_update(inmessage):
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

    fields = ['ts', 'lp', 'pc', 'c', 'o', 'h', 'l', 'v', 'ltq', 'ltp']    
    
    message = { field: inmessage[field] for field in set(fields) & set(inmessage.keys())}

    feedtime = int(inmessage['ft'])
    message['ft'] = str(datetime.datetime.fromtimestamp( feedtime ))
    
    print("quote event: {0}".format(time.strftime('%d-%m-%Y %H:%M:%S')) + str(inmessage))

    print(message)
    
    key = inmessage['e'] + '|' + inmessage['tk']

    if key in SYMBOLDICT:
        symbol_info =  SYMBOLDICT[key]
        symbol_info.update(message)
        SYMBOLDICT[key] = symbol_info
    else:
        SYMBOLDICT[key] = message

    pd.DataFrame.from_dict(SYMBOLDICT).transpose()
    #print(SYMBOLDICT[key])

def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')
    
    api.subscribe(["NSE|22","NSE|13","BSE|522032"], feed_type='t')
    #api.subscribe(['NSE|22', 'BSE|522032'])

#end of callbacks

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)

class ProgramKilled(Exception):
    pass
    
def signal_handler(signum, frame):
    raise ProgramKilled
if __name__=="__main__":   
    
    # Register our signal handler with `SIGINT`(CTRL + C)
    signal.signal(signal.SIGINT, signal_handler) 
    # Register the exit handler with `SIGTSTP` (Ctrl + Z)
    signal.signal(signal.SIGTERM , signal_handler) 

    #start of our program
    api = ShoonyaApiPy()

    #yaml for parameters
    with open('..\\cred.yml') as f:
        cred = yaml.load(f, Loader=yaml.FullLoader)
        print(cred)


    excel_file = 'realtime_excel_feed.xlsx'
    if os.path.exists(excel_file):
        workbook = xlsxwriter.Workbook(excel_file)
        workbook.add_worksheet('Live')
        workbook.close()

    wb1 = xw.Book(excel_file)
    sht = wb1.sheets('Live')

    ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

    if ret != None:   
        ret = api.start_websocket(order_update_callback=event_handler_order_update, subscribe_callback=event_handler_quote_update, socket_open_callback=open_callback)
        
        
                 
        while True:     
            try: 
                if socket_opened == True:

                    time.sleep(5)
                    df = pd.DataFrame().from_dict(SYMBOLDICT).transpose()
                    #print(df)  
                    try:
                        sht.range('A1').value = df

                    except Exception as e:
                        print(e)
                    continue
                else:
                    continue

            except ProgramKilled:
                print("Program killed: running cleanup code")
                break
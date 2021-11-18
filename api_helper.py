from NorenRestApiPy.NorenApi import  NorenApi
from threading import Timer
import pandas as pd
import time

class SymbolItem:
    def __init__(self):
        self.df = None
        self.key = None
        self.counter  = 0
        self.lasttime = 0    

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)


class NorenApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://shoonyatrade.finvasia.com/NorenWClientWeb/', websocket='wss://shoonyatrade.finvasia.com/NorenWS/')

    symboldata = {}

    def watch_time_price_series(self,exchange, token, starttime = None):

        # put todays time in string
        if starttime is None:            
            starttime = time.strftime('%d-%m-%Y') + ' 00:00:00'            

        key = (exchange, token)

        print(key)

        if key in self.symboldata:
            item =  self.symboldata[key]
            return item.df

        return self.add_symbol_to_watch(exchange=exchange, token=token, starttime=starttime)

    def refresh_symbol(self, item):        
        
        exchange = item.key[0]
        token    = item.key[1]

        if item.df.count() != 0:
            lasttime    = item.df['time'].values[0]
            starttime   = get_time(lasttime)

            ret = self.get_time_price_series(exchange=exchange, token=token, starttime=starttime)            
            df = pd.DataFrame.from_dict(ret)        
            df.set_index('ssboe')
            print('**********')
            print(df)


        #start_secs = get_time(starttime)


    def refresh_symbols(self):
        for key in self.symboldata:              
            self.refresh_symbol(self.symboldata[key])
            
            

    def add_symbol_to_watch(self, exchange, token, starttime):
        key = (exchange, token)
        start_secs = get_time(starttime)
        end_time = time.time()            
        
        #get the first frame
        ret = self.get_time_price_series(exchange=exchange, token=token, starttime=start_secs, endtime=end_time)            
        df = pd.DataFrame.from_dict(ret)        
        df.set_index('ssboe')
        #print(df)
        if len(self.symboldata) == 0:
            #need to get close to 00 min
            self.timer = Timer(5,self.refresh_symbols,args=[])
            self.timer.start()
            print('timer starts' )

        item = SymbolItem() 
        item.df = df
        item.key = key

        self.symboldata[key] = item
        #print(self.symboldata.keys())

        #self.refresh_symbols()
        return df
        
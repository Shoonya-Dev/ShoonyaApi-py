from NorenRestApiPy.NorenApi import  NorenApi
from threading import Timer
import pandas as pd
import time
import concurrent.futures

api = None
class Order:
    def __init__(self):
        self.buy_or_sell=''
        self.product_type='C'
        self.exchange=''
        self.tradingsymbol='', 
        self.quantity=0
        self.discloseqty=0
        self.price_type='LMT'
        self.price=0.00
        self.trigger_price=None
        self.retention='DAY'
        self.remarks=''
        self.amo='NO'
        self.bookloss_price = 0.0
        self.bookprofit_price = 0.0
        self.trail_price = 0.0

def place_order(order):
    ret = api.place_order(buy_or_sell=order.buy_or_sell, product_type=order.product_type,
                        exchange=order.exchange, tradingsymbol=order.tradingsymbol, 
                        quantity=order.quantity, discloseqty=order.discloseqty, price_type=order.price_type, 
                        price=order.price, trigger_price=order.trigger_price,
                        retention=order.retention, remarks=order.remarks)
    #print(ret)

    return ret

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')

    return time.mktime(data)


class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://shoonyatrade.finvasia.com/NorenWClientTP/', websocket='wss://shoonyatrade.finvasia.com/NorenWSTP/', eodhost='https://shoonya.finvasia.com/chartApi/getdata/')
        global api
        api = self

    def place_basket(self, orders):

        resp_err = 0
        resp_ok  = 0
        result   = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            future_to_url = {executor.submit(place_order, order): order for order in  orders}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
            try:
                result.append(future.result())
            except Exception as exc:
                print(exc)
                resp_err = resp_err + 1
            else:
                resp_ok = resp_ok + 1

        return result
                
            
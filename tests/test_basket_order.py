import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy, Order
import logging
import yaml
import timeit

#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = ShoonyaApiPy()

#credentials
with open('..\\cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

orders = []

for index in range(1,5):
    order = Order()
    order.buy_or_sell = 'B'
    order.product_type='C'
    order.exchange='NSE'
    order.tradingsymbol='INFY-EQ'
    order.quantity=index
    order.discloseqty=0
    order.price_type='LMT'
    order.price=1500.00
    order.trigger_price=None
    order.retention='DAY'
    order.remarks='my_order_001'

    orders.append(order)

starttime = timeit.default_timer()
ret = api.place_basket(orders)
print("The time difference is :", timeit.default_timer() - starttime)


print(ret)

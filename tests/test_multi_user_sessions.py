import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import time
import yaml
import logging
logging.basicConfig(level=logging.DEBUG)
with open('cred.yml') as f:
    creds_user1 = yaml.load(f, Loader=yaml.FullLoader)
    print(creds_user1)

with open('cred1.yml') as f:
    creds_user2 = yaml.load(f, Loader=yaml.FullLoader)
    print(creds_user2)

#Create two instances to handle multiple accounts.
user1 = ShoonyaApiPy()
user2 = ShoonyaApiPy()

#Login multiple accounts.
ret = user1.login(userid = creds_user1['user'], password = creds_user1['pwd'], 
            twoFA=creds_user1['factor2'], vendor_code=creds_user1['vc'], 
            api_secret=creds_user1['apikey'], imei=creds_user1['imei'])
print(ret)
ret2 = user2.login(userid = creds_user2['user'], password = creds_user2['pwd'], 
            twoFA=creds_user2['factor2'], vendor_code=creds_user2['vc'], 
            api_secret=creds_user2['apikey'], imei=creds_user2['imei'])
print(ret2)
#Individual Websocket callbacks for each account.
def user1_socket_order_update(message):
    print(f"OrderInfo Received for User1:{message}" )

def user1_socket_quote_update(message):
    print(f"Quote Received for User1:{message}")

def user1_socket_open():
    print("websocket is now open for User1:")
    user1.subscribe('NSE|26000')

def user2_socket_order_update(message):
    print(f"OrderInfo Received for User2: {message}")

def user2_socket_quote_update(message):
    print(f"Quote Received for User2:{message}")
def user2_socket_open():
    print("websocket is now open for User2:")
    user2.subscribe('NSE|26000')
#Start the websocket and subscribe to some live feed.
user1.start_websocket(order_update_callback=user1_socket_order_update, 
                      subscribe_callback=user1_socket_quote_update, 
                      socket_open_callback = user1_socket_open)
time.sleep(2)




user2.start_websocket(order_update_callback=user2_socket_order_update, 
                      subscribe_callback=user2_socket_quote_update, 
                      socket_open_callback = user2_socket_open)
time.sleep(2)


print("Both accounts are initialized, now the quotes/order updates should come for both users.")
prompt1=input('what shall we do? ').lower()    
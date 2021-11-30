# NorenApi

Api used to connect to NorenOMS
****

## Build

to build this package and install it on your server please use 

``` pip install -r requirements.txt ```


****

## API 
```NorenApi```
- [login](#md-login)

Symbols
- [searchscrip](#md-searchscrip)
- [get_security_info](#md-get_security_info)
- [get_quotes](#md-get_quotes)

Orders and Trades
- [place_order](#md-place_order)
- [modify_order](#md-modify_order)
- [cancel_order](#md-cancel_order)

Holdings and Limits
- [get_holdings](#md-get_holdings)
- [get_positions](#md-get_positions)

Websocket API
- [start_websocket](#md-start_websocket)
- [subscribe](#md-subscribe)
- [unsubscribe](#md-unsubscribe)

Example
- [getting started](#md-example-basic)
- [Market Functions](#md-example-market)
- [Orders and Trade](#md-example-orders)

#### <a name="md-login"></a> login(userid, password, twoFA, vendor_code, api_secret, imei)
connect to the broker, only once this function has returned successfully can any other operations be performed

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| userid | ```string``` | False | user credentials |
| password | ```string```| False | password encrypted |
| twoFA | ```string``` | False | dob/pan |
| vendor_code | ```string``` | False | vendor code shared  |
| api_secret | ```string``` | False | your secret   |
| imei | ```string``` | False | imei identification |

#### <a name="md-place_order"></a> place_order(buy_or_sell, product_type,exchange, tradingsymbol, quantity, discloseqty, price_type, price=0.0, trigger_price=None, retention='DAY', amo='NO', remarks=None)
place an order to oms

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| buy_or_sell | ```enum``` | False | BuyorSell enum class |
| product_type | ```enum```| False | ProductType enum class |
| exchange | ```string``` | False | Exchange NSE  / NFO / BSE / CDS |
| tradingsymbol | ```string``` | False | Unique id of contract on which order to be placed. (use url encoding to avoid special char error for symbols like M&M |
| quantity | ```integer``` | False | order quantity   |
| discloseqty | ```integer``` | False | order disc qty |
| price_type | ```enum```| False | PriceType enum class |
| price | ```integer```| False | Price in paise, 100.00 is sent as 10000 |
| trigger_price | ```integer```| False | Price in paise |
| retention | ```string```| False | DAY / IOC / EOS |
| amo | ```string```| True | Flag for After Market Order, YES/NO  |
| remarks | ```string```| True | client order id or free text   |

#### <a name="md-modify_order"></a> modify_order(orderno, exchange, tradingsymbol, newquantity,newprice_type, newprice, newtrigger_price, amo):
modify the quantity pricetype or price of an order

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| orderno | ```string``` | False | orderno to be modified |
| exchange | ```string``` | False | Exchange NSE  / NFO / BSE / CDS |
| tradingsymbol | ```string``` | False | Unique id of contract on which order to be placed. (use url encoding to avoid special char error for symbols like M&M |
| newquantity | ```integer``` | False | new order quantity   |
| newprice_type | ```enum```| False | PriceType enum class |
| newprice | ```integer```| False | Price in paise, 100.00 is sent as 10000 |
| newtrigger_price | ```integer```| False | Price in paise |

#### <a name="md-cancel_order"></a> cancel_order(orderno)
cancel an order

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| orderno | ```string``` | False | orderno with status open |

#### <a name="md-get_holdings"></a> get_holdings(product_type)
retrieves the holdings as a list

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| product_type | ```enum``` | True | retreives the delivery holdings or for a given product  |

#### <a name="md-get_positions"></a> get_positions()
retrieves the positions cf and day as a list

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
|  No Parameters  |

#### <a name="md-searchscrip"></a> searchscrip(exchange, searchtext):
search for scrip or contract and its properties  

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| exchange | ```string``` | True | Exchange NSE  / NFO / BSE / CDS |
| searchtext | ```string``` | True | Search Text ie partial or complete text ex: INFY-EQ, INF.. |

the response is as follows,

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| stat | ```string``` | True | ok or Not_ok |
| values | ```string``` | True | properties of the scrip |
| emsg | ```string``` | False | Error Message |

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| exch | ```string``` | True | Exchange NSE  / NFO / BSE / CDS |
| tsym | ```string``` | True | Trading Symbol is the readable Unique id of contract/scrip |
| token | ```string``` | True | Unique Code of contract/scrip |
| pp | ```string``` | True | price precision, in case of cds its 4 ie 100.1234 |
| ti | ```string``` | True | tick size minimum increments of paise for price  |
| ls | ```string``` | True | Lot Size |



#### <a name="md-get_security_info"></a> get_security_info(exchange, token):
gets the complete details and its properties 

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| exchange | ```string``` | True | Exchange NSE  / NFO / BSE / CDS |
| token | ```string``` | True | token number of the contract|

the response is as follows,

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| stat | ```string``` | True | ok or Not_ok |
| values | ```string``` | True | properties of the scrip |
| emsg | ```string``` | False | Error Message |

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| exch | ```string``` | True | Exchange NSE  / NFO / BSE / CDS |
| tsym | ```string``` | True | Trading Symbol is the readable Unique id of contract/scrip |
| cname| ```string``` | True |  |
| symnam| ```string``` | True |  |
| seg| ```string``` | True |  |
| exd| ```string``` | True |  |
| instname| ```string``` | True |  |
| strprc| ```string``` | True |  |
| optt| ```string``` | True |  |
| isin| ```string``` | True |  |
| ti | ```string``` | True |  |
| ls| ```string``` | True |  |
| pp| ```string``` | True |  |
| mult| ```string``` | True |  |
| gp_nd| ```string``` | True |  |
| prcunt| ```string``` | True |  |
| prcqqty| ```string``` | True |  |
| trdunt| ```string``` | True |  |
| delunt| ```string``` | True |  |
| frzqty| ```string``` | True |  |
| gsmind| ```string``` | True |  |
| elmbmrg| ```string``` | True |  |
| elmsmrg| ```string``` | True |  |
| addbmrg| ```string``` | True |  |
| addsmrg| ```string``` | True |  |
| splbmrg| ```string``` | True |  |
| splsmrg| ```string``` | True |  |
| delmrg| ```string``` | True |  |
| tenmrg| ```string``` | True |  |
| tenstrd| ```string``` | True |  |
| tenendd| ```string``` | True |  |
| exestrd| ```string``` | True |  |
| exeendd| ```string``` | True |  |
| elmmrg| ```string``` | True |  |
| varmrg| ```string``` | True |  |
| expmrg| ```string``` | True |  |
| token| ```string``` | True |  |
| prcftr_d| ```string``` | True |  |

#### <a name="md-get_quotes"></a> get_quotes(exchange, token):
gets the complete details and its properties 

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| exchange | ```string``` | True | Exchange NSE  / NFO / BSE / CDS |
| token | ```string``` | True | token number of the contract|

the response is as follows,

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| stat | ```string``` | True | ok or Not_ok |
| values | ```string``` | True | properties of the scrip |
| emsg | ```string``` | False | Error Message |

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| exch | ```string``` | True | Exchange NSE  / NFO / BSE / CDS |
| tsym | ```string``` | True | Trading Symbol is the readable Unique id of contract/scrip |
| cname | ```string``` | True | Company Name |
symname| ```string``` | True |Symbol Name |
seg| ```string``` | True |Segment |
| instname| ```string``` | True |Instrument Name |
| isin| ```string``` | True |ISIN |
| pp| ```string``` | True |Price precision |
| ls| ```string``` | True |Lot Size  |
| ti| ```string``` | True |Tick Size  |
| mult| ```string``` | True |Multiplier |
| uc| ```string``` | True |Upper circuit limitlc |
| lc| ```string``` | True |Lower circuit limit |
| prcftr_d| ```string``` | True |Price factor((GN / GD) * (PN/PD)) |
| token| ```string``` | True |Token |
| lp| ```string``` | True |LTP |
| o| ```string``` | True |Open Price |
| h| ```string``` | True |Day High Price |
| l| ```string``` | True |Day Low Price |
| v| ```string``` | True |Volume |
| ltq| ```string``` | True |Last trade quantity |
| ltt| ```string``` | True |Last trade time |
| bp1| ```string``` | True |Best Buy Price 1 |
| sp1| ```string``` | True |Best Sell Price 1 |
| bp2| ```string``` | True |Best Buy Price 2 |
| sp2| ```string``` | True |Best Sell Price 2 |
| bp3| ```string``` | True |Best Buy Price 3 |
| sp3| ```string``` | True |Best Sell Price 3 |
| bp4| ```string``` | True |Best Buy Price 4 |
| sp4| ```string``` | True |Best Sell Price 4 |
| bp5| ```string``` | True |Best Buy Price 5 |
| sp5| ```string``` | True |Best Sell Price 5 |
| bq1| ```string``` | True |Best Buy Quantity 1 |
| sq1| ```string``` | True |Best Sell Quantity 1 |
| bq2| ```string``` | True |Best Buy Quantity 2 |
| sq2| ```string``` | True |Best Sell Quantity 2 |
| bq3| ```string``` | True |Best Buy Quantity 3 |
| sq3| ```string``` | True |Best Sell Quantity 3 |
| bq4| ```string``` | True |Best Buy Quantity 4 |
| sq4| ```string``` | True |Best Sell Quantity 4 |
| bq5| ```string``` | True |Best Buy Quantity 5 |
| sq5| ```string``` | True |Best Sell Quantity 5 |
| bo1| ```string``` | True |Best Buy Orders 1 |
| so1| ```string``` | True |Best Sell Orders 1 |
| bo2| ```string``` | True |Best Buy Orders 2 |
| so2| ```string``` | True |Best Sell Orders 2 |
| bo3| ```string``` | True |Best Buy Orders 3 |
| so3| ```string``` | True |Best Sell Orders 3 |
| bo4| ```string``` | True |Best Buy Orders 4 |
| so4| ```string``` | True |Best Sell Orders 4 |
| bo5| ```string``` | True |Best Buy Orders 5 |
| so5| ```string``` | True |Best Sell Orders 5|
 
 
 <a name="md-start_websocket"></a> start_websocket()
starts the websocket

| Param | Type | Optional |Description |
| --- | --- | --- | ---|
| subscribe_callback | ```function``` | False | callback for market updates |
| order_update_callback | ```function```| False | callback for order updates |
| socket_open_callback | ```function``` | False | callback when socket is open (reconnection also) |
| socket_close_callback | ```function```| False | callback when socket is closed |

#### <a name="md-subscribe_orders"></a> subscribe_orders()
get order and trade update callbacks

#### <a name="md-subscribe"></a> subscribe([instruments])
send a list of instruments to watch
| Param | Type | Optional |Description |
| --- | --- | --- | -----|
| instruments | ```list``` | False | list of instruments [NSE\|22,CDS\|1] || ```string``` | True |#### <a name="md-unsubscribe"></a> unsubscribe()
send a list of instruments to stop watch

****
## <a name="md-example-basic"></a> Example - Getting Started
First configure the endpoints in the api_helper constructor. 
Thereon provide your credentials and login as follows.

```python
from NorenRestApiPy.NorenApi import PriceType, BuyorSell, ProductType
from api_helper import NorenApiPy, get_time
import logging
import hashlib

logging.basicConfig(level=logging.DEBUG)

#start of our program
api = NorenApiPy()

#credentials
user        = '< user id>'
u_pwd       = '< password >'
factor2     = 'second factor'
vc          = 'vendor code'
app_key     = 'secret key'
imei        = 'uniq identifier'


ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
print(ret)
```

## <a name="md-example-market"></a> Example Symbol/Contract : Example_market.py
This Example shows API usage for finding scrips and its properties

### Search Scrips
The call can be made to get the exchange provided token for a scrip or alternately can search for a partial string to get a list of matching scrips
Trading Symbol:
oSymbolName + ExpDate + 'F' for all data having InstrumentName starting with FUT
oSymbolName + ExpDate + 'P' + StrikePrice for all data having InstrumentName starting with OPT and with OptionType PE
oSymbolName + ExpDate + 'C' + StrikePrice for all data having InstrumentName starting with OPT and with OptionType C
For MCX, F to be ignored for FUT instruments
```
api.searchscrip(exchange='NSE', searchtext='REL')
```
This will reply as following
```
{
    "stat": "Ok",
    "values": [
        {
            "exch": "NSE",
            "token": "18069",
            "tsym": "REL100NAV-EQ"
        },
        {
            "exch": "NSE",
            "token": "24225",
            "tsym": "RELAXO-EQ"
        },
        {
            "exch": "NSE",
            "token": "4327",
            "tsym": "RELAXOFOOT-EQ"
        },
        {
            "exch": "NSE",
            "token": "18068",
            "tsym": "RELBANKNAV-EQ"
        },
        {
            "exch": "NSE",
            "token": "2882",
            "tsym": "RELCAPITAL-EQ"
        },
        {
            "exch": "NSE",
            "token": "18070",
            "tsym": "RELCONSNAV-EQ"
        },
        {
            "exch": "NSE",
            "token": "18071",
            "tsym": "RELDIVNAV-EQ"
        },
        {
            "exch": "NSE",
            "token": "18072",
            "tsym": "RELGOLDNAV-EQ"
        },
        {
            "exch": "NSE",
            "token": "2885",
            "tsym": "RELIANCE-EQ"
        },
        {
            "exch": "NSE",
            "token": "15068",
            "tsym": "RELIGARE-EQ"
        },
        {
            "exch": "NSE",
            "token": "553",
            "tsym": "RELINFRA-EQ"
        },
        {
            "exch": "NSE",
            "token": "18074",
            "tsym": "RELNV20NAV-EQ"
        }
    ]
}
```
### Security Info
This call is done to get the properties of the scrip such as freeze qty and margins
```
api.get_security_info(exchange='NSE', token='22')
```
The response for the same would be 
```
{
   "request_time": "17:43:38 31-10-2020",
   "stat": "Ok",
   "exch": "NSE",
   "tsym": "ACC-EQ",
   "cname": "ACC LIMITED",
   "symname": "ACC",
   "seg": "EQT",
   "instname": "EQ",
   "isin": "INE012A01025",
   "pp": "2",
   "ls": "1",
   "ti": "0.05",
   "mult": "1",
   "prcftr_d": "(1 / 1 ) * (1 / 1)",
   "trdunt": "ACC.BO",
   "delunt": "ACC",
   "token": "22",
   "varmrg": "40.00"
}

```
### Subscribe to a live feed
Subscribe to a single token as follows

```
api.subscribe('NSE|13')
```

Subscribe to a list of tokens as follows
```
api.subscribe(['NSE|22', 'BSE|522032'])
```

First we need to connect to the WebSocket and then subscribe as follows
```
feed_opened = False

def event_handler_feed_update(tick_data):
    print(f"feed update {tick_data}")

def open_callback():
    global feed_opened
    feed_opened = True


api.start_websocket( order_update_callback=event_handler_order_update,
                     subscribe_callback=event_handler_feed_update, 
                     socket_open_callback=open_callback)

while(feed_opened==False):
    pass

# subscribe to a single token 
api.subscribe('NSE|13')

#subscribe to multiple tokens
api.subscribe(['NSE|22', 'BSE|522032'])
```
## <a name="md-example-orders"></a> Example - Orders and Trades : example_orders.py
### Place Order
    Place a Limit order as follows
```
    api.place_order(buy_or_sell=BuyorSell.Buy, product_type=ProductType.Delivery,
                        exchange='NSE', tradingsymbol='INFY-EQ', 
                        quantity=1, discloseqty=0,price_type=PriceType.Limit, price=1500, trigger_price=None,
                        retention='DAY', remarks='my_order_001')
```
    Place a Market Order as follows
```
    api.place_order(buy_or_sell=BuyorSell.Buy, product_type=ProductType.Delivery,
                        exchange='NSE', tradingsymbol='INFY-EQ', 
                        quantity=1, discloseqty=0,price_type=PriceType.Market, price=0, trigger_price=None,
                        retention='DAY', remarks='my_order_001')
```
    Place a StopLoss Order as follows
```
    api.place_order(buy_or_sell=BuyorSell.Buy, product_type=ProductType.Delivery,
                        exchange='NSE', tradingsymbol='INFY-EQ', 
                        quantity=1, discloseqty=0,price_type=PriceType.StopLossLimit, price=1500, trigger_price=1450,
                        retention='DAY', remarks='my_order_001')
```
### Modify Order
    Modify a New Order by providing the OrderNumber
```
    api.modify_order(exchange='NSE', tradingsymbol='INFY-EQ', orderno=orderno,
                                   newquantity=2, newprice_type=PriceType.Limit, newprice=1505)
```
### Cancel Order
    Cancel a New Order by providing the Order Number
```
    api.cancel_order(orderno=orderno)
```
### Subscribe to Order Updates

Connecting to the Websocket will automatically subscribe and provide the order updates in the call back as follows
Note: Feed and Order updates are received from the same websocket and needs to be connected once only.

```
feed_opened = False

def event_handler_order_update(order):
    print(f"order feed {order}")

def open_callback():
    global feed_opened
    feed_opened = True


api.start_websocket( order_update_callback=event_handler_order_update,
                     subscribe_callback=event_handler_feed_update, 
                     socket_open_callback=open_callback)

while(feed_opened==False):
    pass


```

****

## Author

Kumar Anand

****

## License

Copyright (C) 2021 Kambala Solutions Pvt Ltd- All Rights Reserved
Copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
All file transfers are logged.

****



import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging
import yaml
import datetime
import timeit
from concurrent.futures import ThreadPoolExecutor

#supress debug messages for prod/tests
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


#start of our program
api = ShoonyaApiPy()

def getLastQuote(scrip):
    print(f"{scrip['exch']} {scrip['token']}")
    scripdata = api.get_quotes(exchange=scrip['exch'], token=scrip['token'])

    return scripdata

def getLastQuoteOptionChain(exchange, tradingsymbol, strikeprice, count = 10):
    chain = api.get_option_chain(exchange=exch, tradingsymbol=tsym, strikeprice=strikeprice, count=count)

    print(chain)
    
    chainscrips = []
    
    result =[]
    with ThreadPoolExecutor(max_workers=10) as exe:
        # Maps the method 'getLastQuote' with a list of values.
        result = exe.map(getLastQuote,chain['values'])
     
        #for r in result:
        #  print(r)

    return result



#yaml for parameters
with open('..\\cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

if ret != None:   
    starttime = timeit.default_timer()
    print("The start time is :",starttime)  
    
    exch  = 'NFO'
    tsym = 'NIFTY27OCT22F'
    starttime = timeit.default_timer()

    chain = getLastQuoteOptionChain(exchange=exch, tradingsymbol=tsym, strikeprice=16000)

    print("The time to execute is :", timeit.default_timer() - starttime)

    for scrip in chain:
        print(f"{scrip['tsym']} {scrip['lp']}")
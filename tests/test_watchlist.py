import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging
import yaml
import datetime
import timeit

#supress debug messages for prod/tests
logging.basicConfig(level=logging.DEBUG)

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
with open('..\\cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

if ret != None:   
    wlnames = api.get_watch_list_names()

    for wl in wlnames['values']:
        print(80*'=')        
        scrips = api.get_watch_list(wlname=wl)
        print(scrips)
        print(80*'=')        

    wltest = wlnames['values'][0]
    ret = api.add_watch_list_scrip(wlname=wltest, instrument='NSE|22')
    wlscrips = api.get_watch_list(wlname=wltest)

    for scrip in wlscrips['values']:
        print(f"{scrip['exch']} - {scrip['token']} {scrip['tsym']}")
    
    print(80*'=')
    ret = api.delete_watch_list_scrip(wlname=wltest, instrument='NSE|22')
    wlscrips = api.get_watch_list(wlname=wltest)

    for scrip in wlscrips['values']:
        print(f"{scrip['exch']} - {scrip['token']} {scrip['tsym']}")
    
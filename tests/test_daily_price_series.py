import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging
import yaml
import datetime
import timeit

#supress debug messages for prod/tests
logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)


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

usersession='094b87ffc2de10a9c1dd03fe1613e133a1bd358f3a94db428249e7a794197838'
ret = api.set_session(userid= cred['user'], password = cred['pwd'], usertoken= usersession)

end = datetime.datetime.today()
end = end.replace(hour=0, minute=0, second=0, microsecond=0)

start = end - datetime.timedelta(days = 10)

ret = api.get_daily_price_series(exchange='NSE', tradingsymbol='RELIANCE-EQ', startdate=start.timestamp(), enddate=end.timestamp())

print(ret)
from api_helper import StarApiPy, get_time
import datetime
import logging
import time
import pandas as pd
import hashlib

logging.basicConfig(level=logging.DEBUG)

#start of our program
api = StarApiPy()

#credentials
user    = <uid>
pwd     = <password>
factor2 = <2nd factor>
vc      = <vendor code>
app_key = <secret key>
imei    = <imei>

#make the api call
ret = api.login(userid=uid, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

print(ret)


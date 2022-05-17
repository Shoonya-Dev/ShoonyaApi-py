import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging
import yaml

#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = ShoonyaApiPy()
api2 = ShoonyaApiPy()

#credentials
with open('..\\cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])


usersession=ret['susertoken']

ret = api2.set_session(userid= cred['user'], password = cred['pwd'], usertoken= usersession)

pos = api2.get_positions()
print(pos)
pos = api.get_positions()

print(pos)
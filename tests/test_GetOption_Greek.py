import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging
import yaml

#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = ShoonyaApiPy()

#credentials
with open('/home/ubuntu/Desktop/Noren/NorenApi-Py-main/cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

ret = api.option_greek(expiredate ='24-NOV-2022',StrikePrice='150',SpotPrice  = '200',InterestRate  = '100',Volatility = '10',OptionType='CE')

print(ret)

from api_helper import ShoonyaApiPy
import logging
from dotenv import load_dotenv
 
#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = ShoonyaApiPy()

#create .env file to securely access user credentials in program
load_dotenv('/home/akash/Documents/Projects/.env')

#os.getenv() will fetch values from .env file 
#credentials 
uid     = os.getenv('userid')
pwd     = os.getenv('password')
factor2 = <2nd factor>
vc      = os.getenv('vendor_key')
app_key = os.getenv('api_key')
imei    = <imei>

#make the api call
ret = api.login(userid=uid, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

print(ret)


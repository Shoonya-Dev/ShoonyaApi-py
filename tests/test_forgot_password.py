import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import ShoonyaApiPy
import logging

#supress debug messages for prod/tests
logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)


#start of our program
api = ShoonyaApiPy()

#use following if yaml isnt used
user    = <uid>
pan     = <pan>
dob     = <dob>
#userid, pan, dob
ret = api.forgot_password(userid = user, pan=pan, dob=dob)

print(ret)
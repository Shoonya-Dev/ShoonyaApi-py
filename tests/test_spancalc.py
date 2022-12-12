import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import NorenApiPy
import logging
import yaml
from NorenRestApiPy.NorenApi import position

#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = NorenApiPy()

#credentials
with open('/home/ubuntu/Desktop/Noren/NorenApi-Py-main/cred.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = api.login(userid = cred['user'], password = cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

positionlist = []

position1 = position()
position1.prd = 'H'
position1.exch='NFO'
position1.instname = 'FUTSTK'
position1.symname = 'ACC'
position1.exd= '29-DEC-2022'
position1.optt= 'XX'
position1.strprc= '-1'
position1.buyqty= '500'
position1.sellqty= '0'
position1.netqty= '500'
positionlist.append(position1)

position2 = position()
position2.prd = 'H'
position2.exch='NFO'
position2.instname = 'OPTSTK'
position2.symname = 'ACC'
position2.exd= '29-DEC-2022'
position2.optt= 'CE'
position2.strprc= '1120'
position2.buyqty= '250'
position2.sellqty= '0'
position2.netqty= '250'
positionlist.append(position2)

position3= position()
position3.prd = 'H'
position3.exch='NFO'
position3.instname = 'OPTSTK'
position3.symname = 'ACC'
position3.exd= '29-DEC-2022'
position3.optt= 'PE'
position3.strprc='1900'
position3.buyqty= '500'
position3.sellqty= '0'
position3.netqty= '500'
positionlist.append(position3)

position4= position()
position4.prd = 'H'
position4.exch='NFO'
position4.instname = 'FUTIDX'
position4.symname = 'FINNIFTY'
position4.exd= '27-DEC-2022'
position4.optt= 'XX'
position4.strprc= '-1'
position4.buyqty= '80'
position4.sellqty= '0'
position4.netqty= '80'
positionlist.append(position4)

position5= position()
position5.prd = 'H'
position5.exch='NFO'
position5.instname = 'OPTIDX'
position5.symname = 'MIDCPNIFTY'
position5.exd= '06-DEC-2022'
position5.optt= 'PE'
position5.strprc= '4150'
position5.buyqty= '0'
position5.sellqty= '75'
position5.netqty= '-75'
positionlist.append(position5)

position6= position()
position6.prd = 'H'
position6.exch='NFO'
position6.instname = 'OPTIDX'
position6.symname = 'MIDCPNIFTY'
position6.exd= '06-DEC-2022'
position6.optt= 'CE'
position6.strprc= '4150'
position6.buyqty= '0'
position6.sellqty= '75'
position6.netqty= '-75'
positionlist.append(position6)

actid = 'xyz'
senddata = {}
senddata['actid'] =actid
senddata['pos'] = positionlist
#payload = 'jData=' + json.dumps(senddata,default=lambda o: o.encode())
#print(payload)
ret = api.span_calculator(actid,positionlist)
print(ret)
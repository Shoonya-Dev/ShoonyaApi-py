from api_helper import ShoonyaApiPy
import pandas as pd
import yaml
from datetime import datetime
import re
import traceback
import pyotp

def get_expiry_dates(api, exchange, tradingsymbol):
    expiry_dates = set()
    ret = api.searchscrip(exchange=exchange, searchtext=tradingsymbol)
    if ret and 'values' in ret:
        for symbol in ret['values']:
            tsym = symbol['tsym']
            if tsym.startswith(tradingsymbol):
                # e.g. NIFTY25OCT22C17000
                match = re.search(r'\d{2}[A-Z]{3}\d{2}', tsym)
                if match:
                    expiry_dates.add(match.group(0))
    return sorted(list(expiry_dates), key=lambda x: datetime.strptime(x, '%d%b%y'))

def get_option_chain_for_expiry(api, exchange, tradingsymbol, expiry_date):
    # Get the LTP of the underlying
    token = get_token(api, 'NSE', tradingsymbol)
    if not token:
        print(f"Could not find token for {tradingsymbol}")
        return []
    ret = api.get_quotes(exchange='NSE', token=token)
    if not ret or 'lp' not in ret:
        print(f"Could not get quotes for {tradingsymbol}")
        return []

    ltp = float(ret['lp'])

    chain = api.get_option_chain(exchange=exchange, tradingsymbol=f"{tradingsymbol}{expiry_date}", strikeprice=ltp, count=50)

    option_chain = []
    if chain is not None and 'values' in chain:
        for scrip in chain['values']:
            scripdata = api.get_quotes(exchange=scrip['exch'], token=scrip['token'])
            option_chain.append(scripdata)

    return option_chain

def get_token(api, exchange, tradingsymbol):
    if tradingsymbol == 'NIFTY':
        return '26000'
    if tradingsymbol == 'BANKNIFTY':
        return '26009'

    ret = api.searchscrip(exchange=exchange, searchtext=tradingsymbol)
    if ret is not None and 'values' in ret:
        for symbol in ret['values']:
            if symbol['tsym'] == f"{tradingsymbol}-EQ":
                return symbol['token']
    return None

if __name__ == '__main__':
    try:
        with open('cred.yml') as f:
            cred = yaml.load(f, Loader=yaml.FullLoader)

        api = ShoonyaApiPy()

        # Generate TOTP
        totp = pyotp.TOTP(cred['token']).now()

        ret = api.login(userid=cred['user'], password=cred['pwd'], twoFA=totp, vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])

        if ret != None and ret.get('stat') == 'Ok':
            print("Login successful")
            nifty_expiry_dates = get_expiry_dates(api, 'NFO', 'NIFTY')
            print(f"Nifty Expiry Dates: {nifty_expiry_dates}")
            banknifty_expiry_dates = get_expiry_dates(api, 'NFO', 'BANKNIFTY')
            print(f"BankNifty Expiry Dates: {banknifty_expiry_dates}")

            if len(nifty_expiry_dates) < 3 or len(banknifty_expiry_dates) < 3:
                print("Not enough expiry dates found to proceed.")
                exit()
            # Get the option chain for the current, next, and far expiry dates
            nifty_current_expiry = nifty_expiry_dates[0]
            nifty_next_expiry = nifty_expiry_dates[1]
            nifty_far_expiry = nifty_expiry_dates[2]

            banknifty_current_expiry = banknifty_expiry_dates[0]
            banknifty_next_expiry = banknifty_expiry_dates[1]
            banknifty_far_expiry = banknifty_expiry_dates[2]

            nifty_current_option_chain = get_option_chain_for_expiry(api, 'NFO', 'NIFTY', nifty_current_expiry)
            nifty_next_option_chain = get_option_chain_for_expiry(api, 'NFO', 'NIFTY', nifty_next_expiry)
            nifty_far_option_chain = get_option_chain_for_expiry(api, 'NFO', 'NIFTY', nifty_far_expiry)

            banknifty_current_option_chain = get_option_chain_for_expiry(api, 'NFO', 'BANKNIFTY', banknifty_current_expiry)
            banknifty_next_option_chain = get_option_chain_for_expiry(api, 'NFO', 'BANKNIFTY', banknifty_next_expiry)
            banknifty_far_option_chain = get_option_chain_for_expiry(api, 'NFO', 'BANKNIFTY', banknifty_far_expiry)

            # Save the option chain to a CSV file
            df_nifty_current = pd.DataFrame(nifty_current_option_chain)
            df_nifty_next = pd.DataFrame(nifty_next_option_chain)
            df_nifty_far = pd.DataFrame(nifty_far_option_chain)

            df_banknifty_current = pd.DataFrame(banknifty_current_option_chain)
            df_banknifty_next = pd.DataFrame(banknifty_next_option_chain)
            df_banknifty_far = pd.DataFrame(banknifty_far_option_chain)

            print("Writing to excel file...")
            with pd.ExcelWriter('option_chain.xlsx') as writer:
                df_nifty_current.to_excel(writer, sheet_name='NIFTY_Current')
                df_nifty_next.to_excel(writer, sheet_name='NIFTY_Next')
                df_nifty_far.to_excel(writer, sheet_name='NIFTY_Far')

                df_banknifty_current.to_excel(writer, sheet_name='BANKNIFTY_Current')
                df_banknifty_next.to_excel(writer, sheet_name='BANKNIFTY_Next')
                df_banknifty_far.to_excel(writer, sheet_name='BANKNIFTY_Far')
            print("Done.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

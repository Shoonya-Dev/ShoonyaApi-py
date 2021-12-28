import requests
import zipfile
import os
root = 'https://shoonya.finvasia.com/'
masters = ['NSE_symbols.txt.zip', 'NFO_symbols.txt.zip', 'CDS_symbols.txt.zip', 'MCX_symbols.txt.zip'] 


for zip_file in masters:    
    print(f'downloading {zip_file}')
    url = root + zip_file
    r = requests.get(url, allow_redirects=True)
    open(zip_file, 'wb').write(r.content)
    file_to_extract = zip_file.split()
 
    try:
        with zipfile.ZipFile(zip_file) as z:
            z.extractall()
            print("Extracted: ", zip_file)
    except:
        print("Invalid file")

    os.remove(zip_file)
    print(f'remove: {zip_file}')
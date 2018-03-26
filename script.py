from urllib.request import urlopen
from bs4 import BeautifulSoup
import wget
import zipfile
import os
import redis
import pandas as pd

url = 'https://www.bseindia.com/markets/equity/EQReports/Equitydebcopy.aspx'

conn = urlopen(url)
html = conn.read()

soup = BeautifulSoup(html,"lxml")
tag = soup.find(id='btnhylZip')
link = tag.get('href',None)
if link is not None:
	print(link)

zip_name = wget.download(link)
print()

zip_ref = zipfile.ZipFile(zip_name, 'r')
zip_ref.extractall("csv-files/")
csv_file = zip_ref.namelist()[0]
zip_ref.close()

print(csv_file[0:-4])

os.remove(zip_name)

df = pd.read_csv("csv-files/"+csv_file)

df = df[['SC_CODE', 'SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']].copy()
r = redis.Redis(host='localhost', port=6379, db=0)

r.set("csv_file[0:-4]", df.to_msgpack(compress='zlib'))
print(pd.read_msgpack(r.get("csv_file[0:-4]")).head())



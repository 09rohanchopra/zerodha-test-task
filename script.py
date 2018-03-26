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

df_compute = df.copy()
df_compute['PERCENTAGE'] = (df['CLOSE'] - df['OPEN'])/ df['OPEN']


df_gain = df_compute.nlargest(10,['PERCENTAGE']).copy()
df_loose = df_compute.nsmallest(10,['PERCENTAGE']).copy()


for index, row in df.iterrows():
	r.hmset(row['SC_CODE'],row.to_dict())
	r.set("equity:"+row['SC_NAME'],row['SC_CODE'])

for key in r.scan_iter("gain:*"):
	r.delete(key)
for key in r.scan_iter("loose:*"):
	r.delete(key)

for index, row in df_gain.iterrows():
	r.set("gain:"+row['SC_NAME'],row['SC_CODE'])

for index, row in df_loose.iterrows():
	r.set("loose:"+row['SC_NAME'],row['SC_CODE'])


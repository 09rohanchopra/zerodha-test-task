from urllib.request import urlopen
from bs4 import BeautifulSoup
import wget
import zipfile
import os

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

print(csv_file)

os.remove(zip_name)
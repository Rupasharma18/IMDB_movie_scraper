import requests 
import pprint
import json
from bs4 import BeautifulSoup 
url = 'https://www.imdb.com/title/tt0066763/?ref_=tt_rec_tti'
req = requests.get(url)
soup = BeautifulSoup(req.text,"html.parser")
div = soup.find('div', class_='rec_view')

for a in div.find_all('a', href=True): 
    if a.text: 
      link ='https://www.imdb.com'+ a['href']
    print (link)    
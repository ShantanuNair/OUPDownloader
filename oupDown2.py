
from bs4 import BeautifulSoup
import requests
import urllib2
import os
import errno
import json
import time
import random 


def getDoi(year,issue,page):
 #year = '45'
 #issue = 'D1'
 #time.sleep(random.randint(2,5))
 page = '1'
 foldername = 'year'+year
 response = requests.post("https://wrapapi.com/use/sjn/testoup/oup/0.0.7", json={
   "year": year,
   "issue": issue,
   "page": page,
   "wrapAPIKey": "8X6fUU7zDvhD0I8M7AXGDbj5yK4sT8xX"
 })
 # json_data = json.loads(response.text)
 # print json_data
 jason_data = response.json()
 print jason_data['data']['DOIs'][0]
 DOIs = []
 for doi in jason_data['data']["DOIs"]:
   print doi.split("\'")[0]
   url = doi.split("\'")[0]
   DOIs.append(url)

 abstracts = []
 titles = []
 authors = []
 #trying to deal with captcha in year 46 and 42 
 #DOIs.pop(0)
 #DOIs.pop(1)

 try:
     os.makedirs(foldername)
 except OSError as e:
     if e.errno != errno.EEXIST:
         raise
 for url in DOIs:
   #captcha 
   #time.sleep(random.randint(2,5))
   try:
     headers = {'User-Agent': 'Mozilla/5.0'}
     request = urllib2.Request(url, headers=headers)
     page = urllib2.urlopen(request).read()

     soup = BeautifulSoup(page, features="html.parser")

    # print soup.body
     is_captcha_on_page = soup.find(attrs={'class': 'abstract'}) is None
     if is_captcha_on_page:
       print "ERROR: Captcha showed up!"
     abstract = soup.find(attrs={'class': 'abstract'}).p
     title = soup.find(attrs={'class': 'article-title-main'})
     authors = soup.select(".linked-name")
     abstracts.append(abstract)
     titles.append(title)
     ld_json_data_str = soup.find('script', {'type': 'application/ld+json'}).text.encode('utf-8')
     ld_json_data = json.loads(ld_json_data_str)
     keywords = ld_json_data['keywords'] #did 'about' for year 42. 
     uniqueIdentifier = url[url.rfind('/')+1:]
     filename = foldername + '/' + uniqueIdentifier + ".txt"
     print(uniqueIdentifier)
     with open(filename, 'w') as file:
       file.write("TITLE: ")
       file.write(title.text.encode('utf-8'))
       file.write("\n")
       file.write(abstract.text.encode('utf-8'))
       file.write("\n")
       file.write("\nAUTHORS:\n");
       for a in authors:
         print(a.text.encode('utf-8'))
         file.write("\n")
         file.write(a.text.encode('utf-8'))
       file.write("\n")
       file.write("\nKEYWORDS:\n")
       for k in keywords:
         file.write("\n")
         print(k)
         file.write(k)
       file.close()
   except IOError as e:
     # print(e.errno)
     # print(e)
     print url+" NOT PROCESSED! (No Abstract Found)"

if __name__ == "__main__":
 #for i in range(43,47):
   getDoi(str(42),"D1","1");
   getDoi(str(42),"D1","2"); 

 #for i in range(32,40):
  #getDoi(str(i),"suppl_1","1");  
 

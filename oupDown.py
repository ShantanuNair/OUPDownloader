from bs4 import BeautifulSoup
import requests
import urllib2
import os
import errno
from selenium import webdriver

import json
year = '45'
issue = 'D1'
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
try:
    os.makedirs(foldername)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
for url in DOIs:
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
    abstracts.append(abstract)
    titles.append(title)
    filename = foldername + '/' + title.text.replace("/", ".") + ".txt"
    with open(filename, 'w') as file:
      file.write(abstract.text.encode('utf-8'))

  except IOError as e:
    # print(e.errno)
    # print(e)
    print url+" NOT PROCESSED! (No Abstract Found)"




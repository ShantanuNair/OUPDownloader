from bs4 import BeautifulSoup
from random import choice
import requests
import urllib2
import os
import errno
import json
from thread import start_new_thread
import time
import random

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def getDoi(year, issue, page):
  time.sleep(random.randint(2,5))
  foldername = 'year' + year
  response = requests.post("https://wrapapi.com/use/sjn/testoup/oup/0.0.7", json={
    "year": year,
    "issue": issue,
    "page": page,
    "wrapAPIKey": "8X6fUU7zDvhD0I8M7AXGDbj5yK4sT8xX"
  })
  # json_data = json.loads(response.text)
  # print json_data
  jason_data = response.json()
  if jason_data['data'] is None:
    return
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
      request = urllib2.Request(url,headers=headers)
      page = urllib2.urlopen(request).read()

      soup = BeautifulSoup(page, features="html.parser")
      save_data = {}
      # print soup.body
      is_captcha_on_page = soup.select_one(".abstract") is None
      if is_captcha_on_page:
        print "ERROR: Captcha showed up for " + url
        # print(soup.body)
      # print(soup.prettify())

      abstract = soup.select_one(".abstract")
      # print("ABSTRACT: " + abstract.text.encode('utf-8').strip())
      title = soup.find(attrs={'class': 'article-title-main'})
      authors = soup.select(".linked-name")
      print(url + " " + title.text.encode('utf-8'))
      for author in authors:
        print(author.text.encode('utf-8'))
      ld_json_data_str = soup.find('script', {'type': 'application/ld+json'}).text.encode('utf-8')
      ld_json_data = json.loads(ld_json_data_str)
      keywords = ld_json_data['keywords']
      # print(ld_json_data['keywords'])
      print (keywords)

      save_data['title'] = title.text.encode('utf-8')
      save_data['abstract'] = abstract.text.encode('utf-8')
      save_data['authors'] = [author.text.encode('utf-8') for author in authors]
      save_data['keywords'] = ld_json_data['keywords']
      print (save_data)

      abstracts.append(abstract)
      titles.append(title)
      filename = foldername + '/' + title.text.replace("/", ".") + ".txt"

      # print(abstract)
      with open(filename, 'w') as file:
        # file.write(abstract.text.encode('utf-8'))
        json.dump(save_data, file)


    except requests.ConnectionError as e:
      print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
      print(str(e))
    except requests.Timeout as e:
      print("OOPS!! Timeout Error")
      print(str(e))
    except requests.RequestException as e:
      print("OOPS!! General Error")
      print(str(e))
    except KeyboardInterrupt:
      print("Someone closed the program")
    except Exception as e:
      pass
    #   # print(e.errno)
      print(e)
      print url + " NOT PROCESSED! (No Abstract Found)"




# for i in range(40,47):
#   start_new_thread(getDoi, (str(i), "D1", '1'))
#   start_new_thread(getDoi, (str(i), "D1", '2'))
#   print('done ' + str(i))
# print("Done")
#
#
# for i in range(35,40):
#   # getDoi(str(i), "suppl_1", '1')
#   start_new_thread(getDoi,(str(i), "suppl_1", '1'))
#   start_new_thread(getDoi,(str(i), "suppl_1", '2'))


for i in range(24,25):
  start_new_thread(getDoi, (str(i), "1", '1'))
  start_new_thread(getDoi, (str(i), "1", '2'))
  print('done ' + str(i))
print("Done")

c = raw_input("Type something to quit.")
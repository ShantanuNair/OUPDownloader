
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import urllib2
import os
import errno
import json
import time
import random
from thread import start_new_thread


def getDoi(year, issue, pagenum):
    #year = '45'
    #issue = 'D1'
    pagenum = '1'
    foldername = 'year'+year
    response = requests.post("https://wrapapi.com/use/sjn/testoup/oup/0.0.7", json={
        "year": year,
        "issue": issue,
        "page": pagenum,
        "wrapAPIKey": "8X6fUU7zDvhD0I8M7AXGDbj5yK4sT8xX"
    })
    # json_data = json.loads(response.text)
    # print json_data
    jason_data = response.json()
    print jason_data['data']['DOIs'][0]
    DOIs = []
    for doi in jason_data['data']["DOIs"]:
        url = doi.split("\'")[0]
        print url
        DOIs.append(url)

    abstracts = []
    titles = []
    authors = []
    # trying to deal with captcha in year 46 and 42
    # DOIs.pop(0)
    # DOIs.pop(1)

    try:
        os.makedirs(foldername)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    for url in DOIs:
        # captcha
        # time.sleep(random.randint(2,5))
        try:
            uniqueIdentifier = url[url.rfind('/')+1:]
            filename = foldername + '/' + uniqueIdentifier + ".json"
            if os.path.isfile(filename):
              print uniqueIdentifier + " already exists. Skipping."
              continue 
            
            time.sleep(random.randint(2,5))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            ua = UserAgent()
            header = {'User-Agent': str(ua.safari)}

            request = urllib2.Request(url, headers=header)
            page = urllib2.urlopen(request).read()

            soup = BeautifulSoup(page, features="html.parser")
            save_data = {}
            is_noAbstract = soup.find(attrs={'class': 'abstract'}) is None
            # is_captcha_on_page = soup.find("div", {"id": "catptcha"}) is not None
            is_captcha_on_page = soup.find(id="captcha") is not None
            

            if is_noAbstract:
                # print soup.body
                if is_captcha_on_page:
                    print "Catptcha found on page. Skipping this url. url=" + url
                    continue
                print "No abstract found so skipping this url link. url=" + str(is_captcha_on_page)
                continue

            abstract = soup.find(attrs={'class': 'abstract'}).p
            title = soup.find(attrs={'class': 'article-title-main'})
            authors = soup.select(".linked-name")
            abstracts.append(abstract)
            titles.append(title)
            ld_json_data_str = soup.find(
                'script', {'type': 'application/ld+json'}).text.encode('utf-8')
            ld_json_data = json.loads(ld_json_data_str)
            if('keywords' in ld_json_data):
                keywords = ld_json_data['keywords']
            if('about' in ld_json_data):
                about = ld_json_data['about']
            
            save_data['title'] = title.text.encode('utf-8')
            save_data['abstract'] = abstract.text.encode('utf-8')
            save_data['authors'] = [author.text.encode(
                'utf-8') for author in authors]
            if('keywords' in ld_json_data):
                save_data['keywords'] = ld_json_data['keywords']

            if('about' in ld_json_data):
                save_data['about'] = ld_json_data['about']
            print(uniqueIdentifier)
            with open(filename, 'w') as file:
                json.dump(save_data, file)

        except IOError as e:
            print url + \
                " NOT PROCESSED! (No Abstract Found) isCaptcha=" + \
                str(is_captcha_on_page)
    print "Done processing year " + year + " page " + pagenum


if __name__ == "__main__":
    # # for i in range(43,47):
    # getDoi(str(43), "D1", "1")
    # getDoi(str(43), "D1", "2")g

    # for i in range(32,40):
   # getDoi(str(i),"suppl_1","1")
    # for i in range(24, 31):
    #     getDoi(str(i), "1", "1")
    #     getDoi(str(i), "1", "2")
        # start_new_thread(getDoi, (str(i), "1", '1'))
        # start_new_thread(getDoi, (str(i), "1", '2'))
    for i in range(32,40):
        # getDoi(str(i),"suppl_1","1")
        # getDoi(str(i),"suppl_1","2")
        start_new_thread(getDoi, (str(i), "suppl_1", '1'))
        start_new_thread(getDoi, (str(i), "suppl_1", '2'))
        
c = raw_input("Type something to quit.")
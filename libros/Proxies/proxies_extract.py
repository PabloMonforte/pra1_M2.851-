import requests
from bs4 import BeautifulSoup
import concurrent.futures
import csv

#get the list of free proxies
def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

def extract(proxy):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        #change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=1)
        print(r.json(), r.status_code)
    except requests.ConnectionError as err:
        print(repr(err))
    return proxy

def execut():

    proxylist = getProxies()
    #print(len(proxylist))

    with open('proxies.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, delimiter="\n")
        wr.writerow(proxylist)

    with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(extract, proxylist)
import requests
import csv
import concurrent.futures
from proxies_extract import execut

# opens a csv file of proxies and prints out the ones that work with the url in the extract function

execut()
proxylist = []
good_proxies = []
with open('proxies.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\n')
    for row in reader:
        # print(row)
        proxylist.append(row[0])


def extract(proxy):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http': proxy, 'https': proxy}, timeout=2)
        print(r.json(), ' | Works')
        good_proxies.append(proxy)
    except:
        pass
    return proxy



with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(extract, proxylist)

print(good_proxies)

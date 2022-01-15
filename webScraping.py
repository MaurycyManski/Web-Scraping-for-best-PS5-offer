import requests
import json
import os
import argparse
from bs4 import BeautifulSoup


def RTVeuroAGD():
    site = session.get(shops_links['RTVeuroAGD']).text
    doc = BeautifulSoup(site, 'html.parser')

    products = doc.find_all('div', class_='product-row')
    dic = {}
    for i, x in enumerate(products):
        name = x.find('a').string.strip()
        value = x.find('div', class_='price-normal selenium-price-normal').string.strip().\
            replace('\xa0', '').replace('zł', '')+'.00'
        dic[name] = value
    dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
    offers['RTVeuroAGD'] = dic


def MediaMarkt():
    site = session.get(shops_links['MediaMarkt']).text
    doc = BeautifulSoup(site, 'html.parser')

    names = doc.find_all('h2')
    values = doc.find_all('div',  class_="offer")
    for i, x in enumerate(values):
        values[i] = x.find('span', class_='whole')

    dic = {}
    for i, x in enumerate(names):
        names[i] = x.string
        values[i] = values[i].string.strip()+'.00'
        dic[names[i]] = values[i]
    dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
    offers['MediaMarkt'] = dic


def MediaExpert():
    site = session.get(shops_links['MediaExpert']).text
    doc = BeautifulSoup(site, 'html.parser')

    values = doc.find_all(
        'div', {'class': ['main-price is-big', 'main-price for-action-price is-big']})
    num = len(values)
    names = doc.find_all('a', class_='is-animate spark-link', limit=num)
    dic = {}
    for i, x in enumerate(values):
        values[i] = x.text.strip().replace(
            '\u202f', '').replace(' ', '.').replace('.zł', '')
        names[i] = names[i].string.strip()
        dic[names[i]] = values[i]
    dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
    offers['MediaExpert'] = dic


def printing():
    maxx = 0
    for k, v in offers.items():
        for n, p in v.items():
            x = len(n)
            if x > maxx:
                maxx = x

    L, R = (maxx+2, 12)
    RedStart, RedEnd = ('\033[91m', '\033[0m')
    for x, y in offers.items():
        print('\n'+(' '+x+' ').center(L+R, '*'))
        for n, p in y.items():
            string = n.ljust(L, '.')+p+'[pln]'
            RedString = RedStart + string + RedEnd
            if args.filter == None:
                if not empty:
                    if (n, p) not in save[x].items():
                        print(RedString)
                    else:
                        print(string)
                else:
                    print(RedString)
            else:
                for x in args.filter.split():
                    if x.lower() in n.lower():
                        print(string)
                        break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script shows all offers from 3 most popular electromarkets from Poland: RTVeuroAGD, MediaMarkt, MediaExpert. If the script was executed without the --filter parameter, the result is saved in the file, and if a specific offer differs from the previous save, it is highlighted in red. You can modify object of searching by changing links inside shops_links.json file (but keep the same shop site).')
    parser.add_argument('-f', '--filter', type=str, help="Filter result with string keywords. Enter one or multiple keyword in single/double quotes like: -f 'key1 key2 ... '. Filter ignores capital/lowercase keyword letters. When executing script with this parameter, result is not saved to file (so you won't miss any other new offers!) and strings are printed with white color only.")
    args = parser.parse_args()

    # load shops links from file
    with open('shops_links.json') as j:
        shops_links = json.load(j)

    # if file offers.json doesn't exist, create it
    if not os.path.exists('./offers.json'):
        with open('offers.json', 'w') as j:
            pass

    # load previous search result from file
    with open('offers.json') as j:
        empty = False
        try:
            save = json.load(j)
        except ValueError:
            empty = True

    offers = {}
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-charset": "cp1254,ISO-8859-9,utf-8;q=0.7,*;q=0.3",
        "accept-encoding": "gzip,deflate,sdch",
        "accept-language": "tr,tr-TR,en-US,en;q=0.8",
    }

    with requests.Session() as session:
        session.headers = headers

        RTVeuroAGD()
        MediaMarkt()
        MediaExpert()

        printing()

    # save search result to file
    if args.filter == None:
        with open('offers.json', 'w') as j:
            json.dump(offers, j, indent=2)

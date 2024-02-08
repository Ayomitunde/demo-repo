from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
# It is a scraper for a nigerian e-commerce website
# Also contains pagination
s = HTMLSession()

def get_products_links(page):
    url = f'https://shopahome.com/home-kitchen?p={page}'
    links = []
    resp = s.get(url)

    products = resp.html.find('li.item.product.product-item')
    for cars in products:
        links.append(cars.find('a', first = True).attrs['href'])
    return links

def parse_products(url):    
    resp = s.get(url)
    try:
        title = resp.html.find('h1.page-title', first = True).text
        price = resp.html.find('span.price', first = True).text
        vendor = resp.html.find('div.vendor-info a', first = True).text
        avaliable = resp.html.find('div.stock.available span', first = True).text
        sku = resp.html.find('div.value', first = True).text
    except AttributeError as err:
        title = 'None',
        price = 'None',
        vendor = 'None',
        avaliable  = 'None',
        sku = 'None'
        # print(err)
    
    cars45 = {
        'Name':title,
        'Price':price,
        'Vendor': vendor,
        'Avaliability': avaliable,
        'SKU': sku
        
        
    }
    return cars45


def save_csv(results):
    keys = results[0].keys()
    with open('shophome.csv', 'w', encoding = 'utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
def main():
    results = []
    for x in range(1,11):
        print('Getting Page',x)
        urls = get_products_links(x)
        for url in urls:
            results.append(parse_products(url))
        print('Total results: ', len(results))
        save_csv(results)

if __name__ == '__main__':
    main()
import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import dataclass, asdict, fields
import json
import csv

@dataclass 
class cars:
    name : str 
    price : str
    location : str 
    condition : str 
    



def get_html(url, **kwargs):
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    

    if kwargs.get("page"):
        resp = httpx.get(url + str(kwargs.get("page")), headers = headers, follow_redirects = True)
    else:
        resp = httpx.get(url, headers = headers, follow_redirects = True)
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. Page limit exceeded")
        return False
    html = HTMLParser(resp.text)
    return html


def parse_search_pages(html: HTMLParser):
    
    products = html.css('a.car-feature.car-feature--wide-mobile')
    for product in products:
        yield urljoin("https://www.cars45.com/listing",product.css_first("a").attributes["href"])
        # listing = {
        # "name" : extract_txt(product,"p.car-feature__name"),
        # "price":extract_txt(product,"p.car-feature__amount"),
        # "location": extract_txt(product,"p.car-feature__region"),
        # 'condition': extract_txt(product,"span.car-feature__others__item")
        # }
        # yield listing

def parse_cars_page(html: HTMLParser):
    new_item = cars(
         name = extract_txt(html, "h1.main-details__name__title" ),
         price = extract_txt(html, "h5.main-details__name__price"),
         location = extract_txt(html,"p.main-details__region"),
         condition = extract_txt(html, "div.main-details__tags.flex.wrap span"),
         
    )
    return asdict(new_item)
def extract_txt(html, sel):
    try:
        return html.css_first(sel).text(strip = True)
    except AttributeError:
        return None


def export_to_json(products):
     with open("carlistings.json", "w", encoding = 'utf-8') as f:
        json.dump(products, f, ensure_ascii = False, indent = 2)

def export_to_csv(products):
    field_names = [field.name for field in fields(cars)]
    with open("carlistings.csv", "w", encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()
        writer.writerows(products)
    print("saved to csv")
def main():
    cars = []
    baseurl = 'https://www.cars45.com/listing?page='
    for x in range (1,30):
        print(f"Gathering Listings page: {x}")
        html = get_html(baseurl, page = x)
        
        if html is False:
            break
        product_link =  parse_search_pages(html)
        for url in product_link:
            print(url)
            html = get_html(url)
            cars.append(parse_cars_page(html))
            time.sleep(1)

    export_to_json(cars)
    export_to_csv(cars)
if __name__ == "__main__":
    main()
from bs4 import BeautifulSoup
import pprint
import re
import requests
from urllib.parse import urlparse

pp = pprint.PrettyPrinter(indent=4)

in_stock=[]
preorder=[]
out_of_stock=[]

urls = [
        'https://www.fringesport.com/collections/bumper-plates/products/contrast-bumper-plate-sets?variant=38904440772',
        'https://www.fringesport.com/collections/bumper-plates/products/ofw-black-bumper-plate-sets?variant=38904437252',
        'https://www.fringesport.com/collections/bumper-plates/products/ofw-color-bumper-plate-sets?variant=38904438468',
        'https://www.fringesport.com/collections/barbells/products/mens-olympic-wonder-barbell-20kg',
        ]

# Hacky switch-case implementation
def search_domain(url):
    domain = urlparse(url).netloc
    domains = {
            "www.fringesport.com": lambda: fringe_check_stock(url),
    }
    func=domains.get(domain, lambda: print("{}: Domain not found".format(domain)))
    return func()

def fringe_check_stock(url):
    is_preorder = False

    item_html = BeautifulSoup(requests.get(url).text, 'html.parser')
    item_price = item_html.find_all("p", class_="modal_price")[0].find('span').text.strip()
    item_description = item_html.find_all("div", class_="description")[0].text.strip()

    item_sold_out = len(re.findall(r"Sold Out", item_price))
    item_preorder = len(re.findall(r"Pre-Order", item_description))

    if item_sold_out == 1:
        out_of_stock.append(url)
    elif item_preorder == 1:
        preorder.append(url)
    else:
        in_stock.append(url)

for url in urls:
    search_domain(url)

pp.pprint("In stock: {}".format(in_stock))
pp.pprint("Pre-Order: {}".format(preorder))
pp.pprint("Out of stock: {}".format(out_of_stock))

from lxml import html
import requests

DOM = "http://www.dominos.co.uk/menu"

def parse_dominos():
    pass

def get(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    return tree

if __name__ == "__main__":
    tree = get("https://www.dominos.co.uk/menu")
    print html.tostring(tree)
    print tree

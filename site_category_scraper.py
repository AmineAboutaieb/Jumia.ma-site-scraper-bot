import requests
from bs4 import BeautifulSoup
import json
import html5lib

try:
    domain = "https://www.jumia"
    response = requests.get("https://jumia.ma")
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html5lib")
    
    container = soup.find("div", {"class" : "flyout"})
    broad_categories = container.findAll("a", {"class" : "itm"})
    
    categories = []

    for category in broad_categories:
        if(category.has_attr("href") and category["href"] != ""):
            name = category["href"].replace("-", "_").replace("/", "")
            link = category["href"]

            categories.append({"name" : name, "link" : domain+link })


    f = open("./categories.json", "w")
    json.dump(categories, f)
    f.close()

except Exception as exc:
    print("initial request failed...")
    print(exc)

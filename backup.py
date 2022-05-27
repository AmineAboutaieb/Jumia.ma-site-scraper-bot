import requests
from bs4 import BeautifulSoup
import json
import html5lib

# Categories list
categories = [
    {
        "name" : "ordinateursAccessoiresInformatique", 
        "link" : "ordinateurs-accessoires-informatique"
    },
    {
        "name" : "epicerie",
        "link" : "epicerie"
    },
    {
        "name" : "fashionMode",
        "link" : "fashion-mode"
    },
    {
        "name" : "maisonCuisineJardin",
        "link" : "maison-cuisine-jardin",
    },
    {
        "name" : "telephoneTablette",
        "link" : "telephone-tablette"
    },
    {
        "name" : "electroMenager",
        "link" : "mlp-electromenager"
    },
    {
        "name" : "sportsLoisirs",
        "link" : "sports-loisirs"
    },
    {
        "name" : "electronique",
        "link" : "electronique"
    },
    {
        "name" : "bebeJouets",
        "link" : "bebe-puericulture"
    },
]
# Categories list

tech_prods_url = "https://www.jumia.ma/ordinateurs-accessoires-informatique/"

try:

    response = requests.get(tech_prods_url)
    raw_page_content = response.text
    soup = BeautifulSoup(raw_page_content, "html5lib")

    pages_links_container = soup.find("div", {"class" : ["pg-w", "-ptm", "-pbx1"]})

    pages_links = pages_links_container = soup.findAll("a", {"class" : "pg"})
    
    last_link = pages_links[len(pages_links) - 1]['href']
    last_link_arr = last_link.split('page=')[1].split('#')
    number_pages = last_link_arr[0]

    page_template = "{}?page={}#catalog-listing"

    json_prods = []

    for i in range(1, int(number_pages) + 1):
        print("scraping page {}".format(i))
        next_page_link = page_template.format(tech_prods_url, i)
        page_content_response = requests.get(next_page_link)
        page_content = page_content_response.text
    
        prods_soup = BeautifulSoup(page_content, "html5lib")
        prods = prods_soup.findAll("article", {"class": ["prd"]}) 
        

        for prod in prods:
            title = prod.find("h3")
            prc = prod.find("div", {"class" : "prc"})
            img = prod.find("img", {"class", "img"})
            if(title and prc and img):
                if(title.text != "" and prc.text != "" and img['data-src'] != ""):
                    json_prods.append({ "title" : title.text, "price" : prc.text, "image" : img['data-src'] })

    f = open("products.json", "w")
    json.dump(json_prods, f)
    f.close()

except Exception as exc:

    print("Initial scraping request failed...")
    print(exc)

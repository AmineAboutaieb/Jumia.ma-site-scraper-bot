from importlib.resources import path
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import json

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")

PATH = "./chromedriver.exe"
try:
    driver = webdriver.Chrome(PATH)

    time.sleep(4)

    driver.get("https://www.jumia.ma/")

    driver.refresh()


    container = driver.find_element(by=By.CLASS_NAME, value="flyout")

    hover = ActionChains(driver).move_to_element(container)
    hover.perform()

    time.sleep(2)

    s_item_elements = driver.find_elements(by=By.CLASS_NAME, value="s-itm")
    tit_elements = driver.find_elements(by=By.CLASS_NAME, value="tit")

    elements = s_item_elements + tit_elements

    categories = []

    print("Scraping categories...")

    for element in elements:
        href = element.get_attribute("href")
        if(href and ("https://www.jumia.ma/" in href) and href.find("tvs/?display_size") == -1 ):
            name = href.split("//")[1].split("/")[1].replace("-", "_")
            f_href = href.split("/")[3]
            categories.append({"name" : name, "link" : f_href})



    f = open("categories.json", "w")
    json.dump(categories, f)
    f.close()

    print("Created categories.json file...")

    print("All done")

    print("Scraped {} categories".format(len(categories)))

    driver.quit()

except Exception as exc:
    print(exc)
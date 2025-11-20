import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORMS_URL = "https://forms.gle/Wewb4Srp15bBfXSz7"

response = requests.get(ZILLOW_URL)

soup = BeautifulSoup(response.text, "html.parser")

all_links = soup.find_all("a", attrs={"data-test": "property-card-link"})

property_links = [link.get("href") for link in all_links if "zillow" in link.get("href")]

unique_property_links = set(property_links)
property_links = list(unique_property_links)

span = soup.find_all("span", attrs={"data-test": "property-card-price"})
price_list = []
for price in span:
    price_list.append(re.sub(r"[^$0-9\s]", "", price.text).split(" ")[0])

address = soup.find_all(attrs={"data-test": "property-card-addr"})
all_addresses = [address.text.strip().replace("|", "") for address in address]
print(all_addresses)


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


driver = init_driver()
wait = WebDriverWait(driver, 20)

for link, price, address in zip(property_links, price_list, all_addresses):
    driver.get(GOOGLE_FORMS_URL)

    time.sleep(2)

    inputs = driver.find_elements(By.CSS_SELECTOR, 'input.whsOnd.zHQkBf')

    address_field = inputs[0]
    price_field = inputs[1]
    link_field = inputs[2]

    address_field.clear()
    address_field.send_keys(address)
    price_field.clear()
    price_field.send_keys(price)
    link_field.clear()
    link_field.send_keys(link)

    submit_button = driver.find_element(By.XPATH, '//span[text()="Submit"]')
    submit_button.click()

    # wait for thank-you page to load
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//a[contains(text(),"Submit another response")]')
    ))
driver.quit()

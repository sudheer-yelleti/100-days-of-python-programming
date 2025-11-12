import os
import smtplib

import requests
from bs4 import BeautifulSoup

TARGET_PRICE = 120
my_email = "EMAIL_USER"
my_password = os.environ['GMAIL_APP_PASSWORD']

AMAZON_PRODUCT_URL = "https://appbrewery.github.io/instant_pot/"

response = requests.get(AMAZON_PRODUCT_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
price = soup.find(name="span", class_="aok-offscreen").get_text()

price_without_currency = float(price.split("$")[1])
print(price_without_currency)
if price_without_currency <= TARGET_PRICE:
    product_title = soup.find(name="span", class_="a-size-large product-title-word-break").get_text().strip()
    product_title = ' '.join(product_title.split())
    print(product_title)
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        result = connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Amazon Price Alert!\n\n{product_title} is now {price_without_currency}\n\n"
                f"{AMAZON_PRODUCT_URL}".encode("utf-8"),
        )
        print("Email has been sent!")

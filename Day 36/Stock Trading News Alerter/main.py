import os

import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHAVANTAGE_API_KEY = os.environ['ALPHAVANTAGE_API_KEY']
NEWS_API_KEY = os.environ['NEWS_API_KEY']

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_MESSAGING_SERVICE_SID = os.environ['TWILIO_MESSAGING_SERVICE_SID']
RECIPIENT_PHONE_NUMBER = os.environ['RECIPIENT_PHONE_NUMBER']

FROM_WHATSAPP = os.environ['FROM_WHATSAPP']  # Twilio Sandbox number
TO_WHATSAPP = os.environ['TO_WHATSAPP']  # Your verified number

stock_value_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_API_KEY,
}
stock_news_params = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME
}

response = requests.get(STOCK_ENDPOINT, params=stock_value_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for key, value in data.items()][:2]

yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
positive_difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
percentage_difference = positive_difference / yesterday_closing_price * 100

if percentage_difference > 1:
    response = requests.get(NEWS_ENDPOINT, params=stock_news_params)
    response.raise_for_status()
    articles = response.json()["articles"][:3]

    if not articles:
        print("No news articles found.")
    else:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for article in articles:
            message = client.messages.create(
                from_= FROM_WHATSAPP,
                body=f"Headline: {article['title']}\nBrief: {article['description']}",
                to= TO_WHATSAPP
            )
else:
    print("Not enough stock movement.")

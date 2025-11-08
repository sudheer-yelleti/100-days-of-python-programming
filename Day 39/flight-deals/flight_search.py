import logging
import os
from _datetime import datetime, timedelta

import requests

FLIGHT_SEARCH_API_URL = "https://test.api.amadeus.com/v1"
FLIGHT_SEARCH_V2API_URL = "https://test.api.amadeus.com/v2"
FLIGHT_SEARCH_API_KEY = os.environ.get("FLIGHT_SEARCH_API_KEY")
FLIGHT_SEARCH_API_SECRET = os.environ.get("FLIGHT_SEARCH_API_SECRET")

logging.basicConfig(
    level=logging.INFO,  # Minimum logging level
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.access_token = self.get_access_token()

    def get_access_token(self):
        token = ""
        token_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": FLIGHT_SEARCH_API_KEY,
            "client_secret": FLIGHT_SEARCH_API_SECRET
        }
        get_token_url = f"{FLIGHT_SEARCH_API_URL}/security/oauth2/token"
        response = requests.post(url=get_token_url, headers=token_headers, data=body)
        if response.status_code == 200:
            token = response.json()["access_token"]
        else:
            logging.error(f"Error getting access token: {response._content}")

        return token

    def get_iata_code(self, city_name: str) -> str:
        headers = {
            "Authorization": "Bearer " + self.access_token
        }
        params = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS"
        }
        response = requests.get(url=f"{FLIGHT_SEARCH_API_URL}/reference-data/locations/cities", headers=headers,
                                params=params)
        if response.status_code == 200:
            return response.json()["data"][0]["iataCode"]
        else:
            logging.error(f"Error getting IATA code for {city_name}: {response.status_code}")
            return ""

    def get_flight_offers(self, sheet_data: dict):
        today = datetime.today()
        departure_date = today + timedelta(days=10)
        for item in sheet_data:
            headers = {
                "Authorization": "Bearer " + self.access_token
            }
            params = {
                "originLocationCode": "YVR",
                "destinationLocationCode": item["iataCode"],
                "departureDate": departure_date.strftime("%Y-%m-%d"),
                "adults": 1,
                "nonStop": "false",
                "currencyCode": "CAD",
                "max": 5
            }
            response = requests.get(url=f"{FLIGHT_SEARCH_V2API_URL}/shopping/flight-offers", headers=headers,
                                    params=params)
            if response.status_code == 200:
                offers = response.json()["data"]
                if any(offers):
                    min_price = float(offers[0]["price"]["grandTotal"])
                    for offer in offers:
                        offer_price = float(offer["price"]["grandTotal"])
                        if offer_price <= min_price:
                            min_price = offer_price

                    logging.info(f"Lowest price for {item['city']} is {min_price}")
                else:
                    logging.error(f"No offers found for {item['city']}")
            else:
                logging.error(f"Error getting flight offers for {item['city']}: {response.status_code}")

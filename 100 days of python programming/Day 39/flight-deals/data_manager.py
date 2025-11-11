import logging
import os

import requests

SHEETY_AUTH_BEARER_TOKEN = os.environ.get("SHEETY_AUTH_BEARER_TOKEN")
SHEETY_FLIGHT_URL = "https://api.sheety.co/d37f07c1126a821ac217a8acc8c321f9/flightDeals/prices"
SHEETY_HEADERS = {
    "Authorization": SHEETY_AUTH_BEARER_TOKEN,
    "Content-Type": "application/json"
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        pass

    def get_flight_data(self) -> dict:
        response = requests.get(url=SHEETY_FLIGHT_URL, headers=SHEETY_HEADERS).json()
        if any(response["errors"]):
            logging.error(f"Error getting flight data: {response['errors'][0]['detail']}")
            return {}
        else:
            flight_data = response["prices"]
            return flight_data

    def update_iata_code(self, flight_data: dict):
        for item in flight_data:
            id = item["id"]
            iata_code = item["iataCode"]
            body = {
                "price": {
                    "iataCode": iata_code
                }
            }
            response = requests.put(url=f"{SHEETY_FLIGHT_URL}/{id}", json=body, headers=SHEETY_HEADERS)
            if response.status_code != 200:
                logging.error(f"Error updating flight data: {response.text}")

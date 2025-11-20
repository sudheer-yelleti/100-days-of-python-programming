# This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pprint

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager


class FlightDealFinder:
    def __init__(self):
        self.flight_search = FlightSearch()
        self.data_manager = DataManager()
        self.flight_data = FlightData(self.data_manager)
        self.notification_manager = NotificationManager()

        # self.sheet_data = self.flight_data.flight_data
        # Use the below data if sheety api is not available due to rate limiting or other errors.
        self.sheet_data = [
            {"city": "Paris", "iataCode": "PAR", "Lowest Price": 54},
            {"city": "Frankfurt", "iataCode": "FRA", "Lowest Price": 42},
            {"city": "Tokyo", "iataCode": "TYO", "Lowest Price": 485},
            {"city": "Hong Kong", "iataCode": "HKG", "Lowest Price": 551},
            {"city": "Istanbul", "iataCode": "IST", "Lowest Price": 95},
            {"city": "Kuala Lumpur", "iataCode": "KUL", "Lowest Price": 414},
            {"city": "New York", "iataCode": "NYC", "Lowest Price": 240},
            {"city": "San Francisco", "iataCode": "SFO", "Lowest Price": 260},
            {"city": "Dublin", "iataCode": "DBN", "Lowest Price": 378}
        ]

    def run(self):

        for item in self.sheet_data:
            if item["iataCode"] == "":
                item["iataCode"] = self.flight_search.get_iata_code(item["city"])

        # self.data_manager.update_iata_code(self.sheet_data)
        self.flight_search.get_flight_offers(self.sheet_data)
        pprint(self.sheet_data)


run = FlightDealFinder()
run.run()

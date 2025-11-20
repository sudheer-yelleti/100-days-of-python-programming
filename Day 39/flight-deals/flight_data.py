from data_manager import DataManager


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, data_manager: DataManager):
        # self.flight_data = data_manager.get_flight_data()

        self.price = ""
        self.destination_airport_code = ""

    def find_cheapest_flight(self):
        pass

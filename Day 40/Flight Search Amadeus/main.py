from datetime import datetime, timedelta

from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

for row in sheet_data:
    if row["IATA Code"] == "":
        row["IATA Code"] = flight_search.get_destination_code(row["City"])

print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

# ==================== Search for Flights and Send Notifications ====================

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['City']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["IATA Code"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flights is None or not flights['data']:
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["IATA Code"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_Direct=str(False).lower()
        )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['City']}: £{cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["Lowest Price"]:
        email_list = data_manager.get_customer_emails()
        if len(email_list) > 0:

            if cheapest_flight.stops < 1:
                subject = (
                    f"Low price alert! Only GBP {cheapest_flight.price}to fly from London to {destination['City']}\n"
                    f", departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}.")
            else:
                subject = (
                    f"Low price alert! Only GBP {cheapest_flight.price} to fly from London to {destination['City']}\n"
                    f", with {cheapest_flight.stops} stop(s) departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}.")
            for email in email_list:
                notification_manager.send_email(email, subject)

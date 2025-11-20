import os

import requests
from twilio.rest import Client

# ---------------------------- CONSTANTS ---------------------------- #
OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_MESSAGING_SERVICE_SID = os.environ['TWILIO_MESSAGING_SERVICE_SID']
RECIPIENT_PHONE_NUMBER = os.environ['RECIPIENT_PHONE_NUMBER']

# ---------------------------- GET LOCATION ---------------------------- #
ip_response = requests.get("https://api.ipify.org?format=json")
public_ip = ip_response.json()["ip"]

geo_response = requests.get(f"http://ip-api.com/json/{public_ip}")
geo_data = geo_response.json()
latitude = geo_data["lat"]
longitude = geo_data["lon"]

# ---------------------------- FETCH WEATHER DATA ---------------------------- #
weather_params = {
    "appid": OPENWEATHER_API_KEY,
    "lat": latitude,
    "lon": longitude,
    "cnt": 4,  # Next 4 three-hour forecast periods (~12 hours)
}

weather_response = requests.get(OPENWEATHER_API_URL, params=weather_params)
weather_response.raise_for_status()
forecast_data = weather_response.json()

# ---------------------------- CHECK FOR RAIN ---------------------------- #
will_rain = any(
    any(200 <= condition["id"] < 600 for condition in forecast["weather"])
    for forecast in forecast_data["list"]
)
# ---------------------------- SEND ALERT ---------------------------- #
if will_rain:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID,
        body="🌧️ Heads up! It’s going to rain today. Don’t forget your umbrella!",
        to=RECIPIENT_PHONE_NUMBER,
    )
    print(f"Message sent: {message.sid}")
else:
    print("No rain expected today.")

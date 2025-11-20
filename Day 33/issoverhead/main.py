import logging
import os
import smtplib
import time
from datetime import datetime, timezone

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
my_email = "sudheer.167@gmail.com"
my_password = os.environ['GMAIL_APP_PASSWORD']
# Get the public IP address
ip_request = requests.get('https://api.ipify.org?format=json')
ip_address = ip_request.json()['ip']

# Get geolocation data based on the IP address
geo_request = requests.get(f'http://ip-api.com/json/{ip_address}')
geo_data = geo_request.json()
MY_LATITUDE = geo_data['lat']
MY_LONGITUDE = geo_data['lon']


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_position_data = response.json()

    iss_latitude = float(iss_position_data["iss_position"]["latitude"])
    iss_longitude = float(iss_position_data["iss_position"]["longitude"])

    return (MY_LATITUDE - 5 <= iss_latitude <= MY_LATITUDE + 5 and
            MY_LONGITUDE - 5 <= iss_longitude <= MY_LONGITUDE + 5)


def is_night():
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    current_location_data = response.json()
    sunrise = int(current_location_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(current_location_data["results"]["sunset"].split("T")[1].split(":")[0])

    current_hour = datetime.now(timezone.utc).hour

    return current_hour > sunset or current_hour < sunrise


def send_email(to_email, subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            to_addrs=to_email,
            from_addr=my_email,
            msg=f"Subject:{subject}\n\n{body}"
        )


while True:
    try:
        if is_iss_overhead() and is_night():
            send_email(to_email=my_email, subject="Look Up", body="The ISS is above you in the sky.")
        else:
            logging.info("No ISS overhead right now.")
    except Exception as e:
        logging.error(f"Error: {e}")

    time.sleep(60)

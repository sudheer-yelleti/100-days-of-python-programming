import logging
import os
from datetime import date, datetime

import requests

# ---------------------------- SETUP LOGGING ---------------------------- #
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ---------------------------- CONSTANTS ---------------------------- #
API_NINJAS_KEY = os.environ.get("API_NINJAS_KEY")
SHEETY_AUTH_BEARER_TOKEN = os.environ.get("SHEETY_AUTH_BEARER_TOKEN")

CALORIES_API_URL = "https://api.api-ninjas.com/v1/caloriesburned"
WORKOUT_SHEETY_URL = "https://api.sheety.co/d37f07c1126a821ac217a8acc8c321f9/sudheerWorkouts/workouts"

# ---------------------------- HEADERS ---------------------------- #
API_NINJAS_HEADERS = {
    "X-Api-Key": API_NINJAS_KEY
}

SHEETY_HEADERS = {
    "Authorization": SHEETY_AUTH_BEARER_TOKEN,
    "Content-Type": "application/json"
}

# ---------------------------- API CALL TO FETCH CALORIES ---------------------------- #
calorie_query_params = {
    "activity": "cricket",
    "weight": 55,
    "duration": 4
}

try:
    calorie_response = requests.get(
        CALORIES_API_URL,
        headers=API_NINJAS_HEADERS,
        params=calorie_query_params,
        timeout=10
    )
    calorie_response.raise_for_status()
except requests.RequestException as e:
    logging.error(f"Error fetching calorie data: {e}")
    raise SystemExit(e)

calorie_data = calorie_response.json()
logging.info(f"Calories API returned {len(calorie_data)} activity record(s).")

# ---------------------------- LOG WORKOUT DATA ---------------------------- #
for activity_record in calorie_data:
    activity_name = activity_record["name"]
    activity_duration = activity_record["duration_minutes"]
    calories_burned = activity_record["total_calories"]

    workout_date = date.today().strftime("%d/%m/%Y")
    workout_time = datetime.now().strftime("%H:%M:%S")

    workout_payload = {
        "workout": {
            "date": workout_date,
            "time": workout_time,
            "exercise": activity_name,
            "duration": activity_duration,
            "calories": calories_burned
        }
    }

    try:
        sheety_response = requests.post(WORKOUT_SHEETY_URL, json=workout_payload, headers=SHEETY_HEADERS, timeout=10)
        sheety_response.raise_for_status()
        logging.info(f"Workout '{activity_name}' uploaded successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to upload workout data: {e}")

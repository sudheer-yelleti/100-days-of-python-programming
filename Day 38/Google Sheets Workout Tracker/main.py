import logging
from datetime import date, datetime
import os
import requests

# ---------------------------- CONSTANTS ---------------------------- #
API_NINJAS_KEY = os.environ.get("API_NINJAS_KEY")
CALORIES_API_URL = "https://api.api-ninjas.com/v1/caloriesburned"
WORKOUT_SHEETY_URL = "https://api.sheety.co/d37f07c1126a821ac217a8acc8c321f9/sudheerWorkouts/workouts"

HEADERS = {
    "X-Api-Key": API_NINJAS_KEY,
    "Content-Type": "application/json"
}

# ---------------------------- API CALL TO FETCH CALORIES ---------------------------- #
calorie_query_params = {
    "activity": "cricket",
    "weight": 55,
    "duration": 4
}

calorie_response = requests.get(
    CALORIES_API_URL,
    headers=HEADERS,
    params=calorie_query_params
)

print(calorie_response.text)
calorie_data = calorie_response.json()

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

    sheety_response = requests.post(WORKOUT_SHEETY_URL, json=workout_payload, headers=HEADERS)

    if sheety_response.status_code == 200:
        logging.info("Workout data uploaded successfully.")
    else:
        logging.error(f"Failed to upload data. Status code: {sheety_response.status_code}")

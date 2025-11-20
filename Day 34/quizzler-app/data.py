import requests

parameters = {
    "amount": 10,
    "type": "boolean",
}
quiz_questions = requests.get("https://opentdb.com/api.php", params=parameters)
question_data = quiz_questions.json()["results"]

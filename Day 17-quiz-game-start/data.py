import requests

# Get the qiuz questions from Open Trivia Database.
api_url = "https://opentdb.com/api.php?amount=10&type=boolean"
response = requests.get(api_url)
if (response.status_code == 200):
    question_data = response.json()
else:
    question_data = []
    print(f"There was a problem getting the data from {api_url}. Please try again later.")

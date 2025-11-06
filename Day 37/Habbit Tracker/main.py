import logging
import os
from datetime import datetime

import requests
from tenacity import retry, wait_exponential, stop_after_attempt

# ---------------------------- CONFIGURATION ---------------------------- #
PIXELA_API_URL = "https://pixe.la/v1/users"
PIXELA_USER_NAME = "sudheer60"
PIXELA_GRAPH_ID = "a9x-b2"
PIXELA_TOKEN = os.environ.get("PIXELA_TOKEN", "your-secret-token-here")  # use env variable in production

HEADERS = {"X-USER-TOKEN": PIXELA_TOKEN}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------- UTILITIES ---------------------------- #
def log_response(action: str, response: requests.Response):
    """Log detailed API responses with context."""
    if response.ok:
        logging.info(f"{action} succeeded: {response.status_code}")
    elif response.status_code == 409:
        logging.warning(f"{action} skipped (already exists). Message: {response.text}")
    else:
        logging.error(f"{action} failed: {response.text}")


# ---------------------------- PIXELA OPERATIONS ---------------------------- #
def create_user():
    """Create Pixela user account."""
    params = {
        "token": PIXELA_TOKEN,
        "username": PIXELA_USER_NAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    response = requests.post(PIXELA_API_URL, json=params)
    log_response("Create User", response)
    return response


def create_graph():
    """Create a Pixela graph."""
    params = {
        "id": PIXELA_GRAPH_ID,
        "name": "Coding Graph",
        "unit": "min",
        "type": "float",
        "color": "sora",
    }
    response = requests.post(f"{PIXELA_API_URL}/{PIXELA_USER_NAME}/graphs", json=params, headers=HEADERS)
    log_response("Create Graph", response)
    return response


@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def post_pixel(quantity: float):
    """Post daily data to the graph."""
    data = {
        "date": datetime.now().strftime("%Y%m%d"),
        "quantity": str(quantity)
    }
    response = requests.post(f"{PIXELA_API_URL}/{PIXELA_USER_NAME}/graphs/{PIXELA_GRAPH_ID}",
                             json=data, headers=HEADERS)
    log_response("Post Pixel", response)
    return response


def update_pixel(quantity: float):
    """Update a previously posted pixel."""
    date_string = datetime.now().strftime("%Y%m%d")
    data = {"quantity": str(quantity)}
    response = requests.put(f"{PIXELA_API_URL}/{PIXELA_USER_NAME}/graphs/{PIXELA_GRAPH_ID}/{date_string}",
                            json=data, headers=HEADERS)
    log_response("Update Pixel", response)
    return response


def delete_pixel():
    """Delete today's pixel entry."""
    date_string = datetime.now().strftime("%Y%m%d")
    response = requests.delete(f"{PIXELA_API_URL}/{PIXELA_USER_NAME}/graphs/{PIXELA_GRAPH_ID}/{date_string}",
                               headers=HEADERS)
    log_response("Delete Pixel", response)
    return response


def open_graph():
    """Open the Pixela graph in the default browser."""
    import webbrowser
    url = f"https://pixe.la/v1/users/{PIXELA_USER_NAME}/graphs/{PIXELA_GRAPH_ID}.html"
    webbrowser.open(url)
    logging.info(f"Opened graph URL: {url}")


# ---------------------------- MAIN EXECUTION ---------------------------- #
if __name__ == "__main__":
    logging.info("Starting Pixela API workflow...")

    create_user()
    create_graph()
    post_pixel(120)  # Example: 120 minutes of coding
    update_pixel(180)  # Update the same day's pixel
    delete_pixel()  # Optional: delete today's entry

    open_graph()

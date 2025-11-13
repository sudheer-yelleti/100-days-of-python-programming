import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

GYM_URL = "https://appbrewery.github.io/gym/"
USER_EMAIL = os.environ["EMAIL_USER"]
USER_PASS = os.environ["GYM_MEMBERSHIP_PASSWORD"]


def init_driver():
    """Initialize and return a Chrome WebDriver with a persistent profile."""
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.add_experimental_option("detach", True)

    profile_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_opts.add_argument(f"user-data-dir={profile_dir}")

    driver = webdriver.Chrome(options=chrome_opts)
    return driver


browser = init_driver()
browser.get(GYM_URL)

waiter = WebDriverWait(browser, 10)

# 1. Click login
login_btn = waiter.until(EC.element_to_be_clickable((By.ID, "login-button")))
login_btn.click()

# 2. Enter credentials
email_input = waiter.until(EC.visibility_of_element_located((By.ID, "email-input")))
pass_input = waiter.until(EC.visibility_of_element_located((By.ID, "password-input")))
submit_btn = waiter.until(EC.element_to_be_clickable((By.ID, "submit-button")))

email_input.send_keys(USER_EMAIL)
pass_input.send_keys(USER_PASS)
submit_btn.click()

# 3. Wait for the schedule page to load
waiter.until(EC.presence_of_element_located((By.ID, "schedule-page")))

# 4. Find a class and book it.
day_groups = browser.find_elements(By.CSS_SELECTOR, "div[id^='day-group-']")

for day_el in day_groups:
    day_title = day_el.find_element(By.TAG_NAME, "h2").text
    day_title = day_title.split("(")[1].replace('(', '').replace(')', '')
    if "Fri" in day_title:

        class_cards = day_el.find_elements(By.CSS_SELECTOR, "div[id^='class-card']")
        for card_el in class_cards:
            class_time = card_el.get_attribute("data-class-id").split("-")[-1]
            class_name = card_el.find_element(By.TAG_NAME, "h3").text

            if class_time == "0800":
                book_class_button = card_el.find_element(By.CSS_SELECTOR, "button[id^='book-button']")
                if book_class_button.text == "Waitlisted":
                    print(f"Already on the waitlist: {class_name} on {day_title}")
                elif book_class_button.text == "Booked":
                    print(f"Already booked: {class_name} class on {day_title}")
                elif book_class_button.text == "Join Waitlist":
                    book_class_button.click()
                    print(f"Joined waitlist for: {class_name} on {day_title}")
                else:
                    book_class_button.click()
                    print(f"Booked {class_name} class on {day_title}")
                break
        break

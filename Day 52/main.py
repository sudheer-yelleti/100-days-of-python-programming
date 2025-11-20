import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


driver = init_driver()
wait = WebDriverWait(driver, 20)

driver.get("https://www.instagram.com/")

# --- Login ---
username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(os.environ["INSTAGRAM_USERNAME"])
password_input.send_keys(os.environ["INSTAGRAM_PASSWORD"])
password_input.submit()

time.sleep(3.7)

# --- Navigate to the profile ---
ACCOUNT = "chefsteps"
driver.get(f"https://www.instagram.com/{ACCOUNT}/")

# Ensure profile page is loaded
wait.until(EC.presence_of_element_located((By.XPATH, "//header")))

time.sleep(2)  # allow React event handlers to attach

# --- NOW click followers link ---
followers_link = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
)

followers_link.click()
print("🔥 Followers link clicked!")

# --- Wait for modal ---
followers_modal = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
)

print("✅ Followers modal is open!")


# followers_modal is your dialog element

def find_scrollable_element(driver):
    dialog = driver.find_element(By.XPATH, "//div[@role='dialog']")
    divs = dialog.find_elements(By.TAG_NAME, "div")

    for d in divs:
        try:
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", d)
            client_height = driver.execute_script("return arguments[0].clientHeight", d)

            # Scrollable div = scrollHeight > clientHeight
            if scroll_height > client_height + 50:
                return d
        except:
            continue
    return None


scroll_box = find_scrollable_element(driver)

if scroll_box is None:
    raise Exception("Could not find scrollable followers list container.")
else:
    print("Found scrollable followers container!")

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException

previous_height = 0
follows_clicked = 0

for _ in range(30):  # adjust scroll cycles as needed
    buttons = scroll_box.find_elements(By.XPATH, ".//button")

    for btn in buttons:
        try:
            label = btn.text.strip().lower()
            if label == "follow":
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(0.3)
                btn.click()
                follows_clicked += 1
                print("Followed:", follows_clicked)
                time.sleep(1.2)  # throttle to avoid rate limit

        except (ElementClickInterceptedException, StaleElementReferenceException):
            continue

    # scroll down the popup
    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
        scroll_box
    )
    time.sleep(1)

    current_height = driver.execute_script("return arguments[0].scrollTop", scroll_box)
    if current_height == previous_height:
        print("Reached end of list.")
        break
    previous_height = current_height

print("Total followed:", follows_clicked)

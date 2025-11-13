import logging
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

GAME_URL = "https://ozh.github.io/cookieclicker/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
TIME_INTERVAL_TO_CHECK_FOR_UPGRADE = 5  # Interval (in seconds) to check for available upgrades


def create_webdriver():
    """Initialize and return a Chrome WebDriver with a custom user-agent."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(f"user-agent={USER_AGENT}")

    driver = webdriver.Chrome(options=chrome_options)

    return driver


# Set script runtime (5 minutes)
timeout_seconds = 5 * 60
start_time = time.time()
end_time = start_time + timeout_seconds
last_upgrade_check_time = time.time()  # Track last upgrade time

# Launch browser and open game
browser = create_webdriver()
browser.get(GAME_URL)

wait = WebDriverWait(browser, 10)

# Select English language
wait.until(EC.presence_of_element_located((By.ID, "langSelect-EN")))
language_button = browser.find_element(By.ID, "langSelect-EN")
language_button.click()

# Locate the main cookie
wait.until(EC.presence_of_element_located((By.ID, "bigCookie")))
cookie_button = browser.find_element(By.ID, "bigCookie")
browser.refresh()

# Main game loop
while time.time() < end_time:
    try:
        # Click the main cookie
        cookie_button = browser.find_element(By.ID, "bigCookie")
        cookie_button.click()
        time.sleep(0.001)  # 1 ms pause between clicks

        # Check for upgrades periodically
        if time.time() - last_upgrade_check_time > TIME_INTERVAL_TO_CHECK_FOR_UPGRADE:
            last_upgrade_check_time = time.time()

            # Wait until unlocked products have prices visible
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.product.unlocked.enabled span.price")
            ))
            product_price_elements = browser.find_elements(
                By.CSS_SELECTOR, "div.product.unlocked.enabled span.price"
            )
            current_cookies_element = browser.find_element(By.ID, "cookies")

            # Extract numeric prices from elements
            unlocked_upgrade_prices = [
                int(element.text.replace(",", "")) for element in product_price_elements
            ]
            # max_price = max(unlocked_upgrade_prices)
            current_cookies = int(current_cookies_element.text.replace(",", "").split(" ")[0])

            affordable = [element for element in unlocked_upgrade_prices if element <= current_cookies]
            print("affordable prices")
            print(affordable)
            if affordable:
                max_price = max(affordable)

                # Buy the most expensive upgrade we can afford
                if current_cookies >= max_price:
                    index = unlocked_upgrade_prices.index(max_price)
                    upgrade_button = browser.find_element(
                        By.CSS_SELECTOR, f"div#product{index}.product.unlocked.enabled"
                    )
                    upgrade_button.click()

    except Exception as e:
        logging.exception(f"An error occurred: {e}")
        browser.quit()
        break
try:
    cookies_element = browser.find_element(by=By.ID, value="cookies")
    print(f"Final result: {cookies_element.text}")
except NoSuchElementException:
    print("Couldn't get final cookie count")
finally:
    browser.quit()

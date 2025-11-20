"""
Simple Selenium automation utilities used for practice projects.

This module currently provides helpers to:
- Launch a detached Chrome WebDriver (`create_webdriver`).
- Scrape upcoming Python events from python.org and log their names and dates
  (`get_event_dates_and_names`).
- Retrieve and log Wikipedia's article count from the main page (`wikipedia_stats`).

Note:
- Functions here are intentionally minimal and primarily log the scraped data.
  They do not return the collected values; adapt them if your use case requires
  returning data structures instead of logging.
"""

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
web_driver = None
FORM_SUBMIT_URL = "https://secure-retreat-92358.herokuapp.com/"
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Main_Page"
PYTHON_EVENTS_URL = "https://www.python.org/events/python-events/"


def create_webdriver():
    """Create and return a detached Chrome WebDriver instance.

    The returned driver is created with the Chrome option `detach=True` so that
    the browser window remains open after the script finishes. This is useful
    during development and debugging.

    Returns:
        selenium.webdriver.Chrome: A configured Chrome WebDriver instance.

    Raises:
        selenium.common.exceptions.WebDriverException: If Chrome or the driver
            cannot be started.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_event_dates_and_names(driver):
    """Fetch and log upcoming Python event names and dates from python.org.

    This function navigates to the Python events page, waits for the list to be
    present, extracts event names and dates, builds an `events` dictionary, and
    logs the intermediate lists and final dictionary. It does not return the
    collected data.

    Args:
        driver (selenium.webdriver.remote.webdriver.WebDriver): An active
            Selenium WebDriver used for navigation and element lookup.

    Side Effects:
        - Navigates the provided browser to python.org.
        - Logs the lists of event names, event dates, and the combined mapping.

    Notes:
        If you need the `events` dictionary for further processing, modify the
        function to return it.
    """
    driver.get(PYTHON_EVENTS_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-recent-events time")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".event-title a")))
    event_date_elements = driver.find_elements(By.CSS_SELECTOR, ".list-recent-events time")
    event_name_elements = driver.find_elements(By.CSS_SELECTOR, ".event-title a")

    event_names = [event_name.text for event_name in event_name_elements]
    event_dates = [event_date.text for event_date in event_date_elements]
    logging.info(event_names)
    logging.info(event_dates)

    events = {}
    for n in range(len(event_names)):
        events[n] = {
            "name": event_names[n],
            "date": event_dates[n]
        }
    logging.info(events)


def wikipedia_stats(driver):
    """Retrieve and log Wikipedia's article count from the main page.

    Navigates to Wikipedia's main page and locates the "Special:Statistics"
    link within the article count widget, then logs the visible article count
    text. Intended for demonstration purposes and does not return data.

    Args:
        driver (selenium.webdriver.remote.webdriver.WebDriver): An active
            Selenium WebDriver used for navigation and element lookup.

    Side Effects:
        - Navigates the provided browser to en.wikipedia.org.
        - Logs the extracted article count text, if found.
    """
    driver.get(WIKIPEDIA_URL)
    div_id = "articlecount"
    css_selector = f"div#{div_id} > ul li a[title = 'Special:Statistics']"
    article_count = driver.find_elements(By.CSS_SELECTOR, css_selector)
    for element in article_count:
        logging.info(element.text)


def submit_form(driver):
    driver.get(FORM_SUBMIT_URL)
    first_name_element = driver.find_element(By.NAME, "fName")
    last_name_element = driver.find_element(By.NAME, "lName")
    email_element = driver.find_element(By.NAME, "email")
    first_name_element.send_keys("John")
    last_name_element.send_keys("Doe")
    email_element.send_keys("xyx@xf.com")
    button = driver.find_element(By.CSS_SELECTOR, ".btn")
    button.click()
try:
    web_driver = create_webdriver()
    get_event_dates_and_names(web_driver)
    wikipedia_stats(web_driver)
    submit_form(web_driver)



except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    web_driver.quit()

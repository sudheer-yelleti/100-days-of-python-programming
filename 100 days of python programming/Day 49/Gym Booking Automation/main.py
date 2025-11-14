import os

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

GYM_URL = "https://appbrewery.github.io/gym/"
USER_EMAIL = os.environ["EMAIL_USER"]
USER_PASS = os.environ["GYM_MEMBERSHIP_PASSWORD"]

booked_classes_count = 0
waitlisted_classes_count = 0
already_booked_count = 0
total_tuesday_classes = 0




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

processed_classes = []

for day_el in day_groups:
    day_title = day_el.find_element(By.TAG_NAME, "h2").text
    day_title = day_title.split("(")[-1].replace('(', '').replace(')', '')
    if "Tue" in day_title or "Fri" in day_title:

        class_cards = day_el.find_elements(By.CSS_SELECTOR, "div[id^='class-card']")
        for card_el in class_cards:
            class_time = card_el.get_attribute("data-class-id").split("-")[-1]
            class_name = card_el.find_element(By.TAG_NAME, "h3").text
            class_info = f"{class_name} on {day_title}"
            if class_time == "1800":
                book_class_button = card_el.find_element(By.CSS_SELECTOR, "button[id^='book-button']")
                if book_class_button.text == "Waitlisted":
                    print(f"Already on the waitlist: {class_name} on {day_title}")
                    already_booked_count += 1
                    processed_classes.append(f"[Waitlisted] {class_info}")
                elif book_class_button.text == "Booked":
                    print(f"Already booked: {class_name} class on {day_title}")
                    already_booked_count += 1
                    processed_classes.append(f"[Booked] {class_info}")
                elif book_class_button.text == "Join Waitlist":
                    book_class_button.click()
                    print(f"Joined waitlist for: {class_name} on {day_title}")
                    waitlisted_classes_count += 1
                    processed_classes.append(f"[New Waitlist] {class_info}")
                else:
                    book_class_button.click()
                    print(f"Booked {class_name} class on {day_title}")
                    booked_classes_count += 1
                    processed_classes.append(f"[New Booking] {class_info}")

total_booked = already_booked_count + booked_classes_count + waitlisted_classes_count
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

my_bookings_link = browser.find_element(By.LINK_TEXT, "My Bookings")
my_bookings_link.click()

verified_count = 0
waiter.until(EC.presence_of_element_located((By.ID, "my-bookings-page")))

all_cards = browser.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
for card in all_cards:
    try:
        when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        when_text = when_paragraph.text
        if ("Tue" in when_text or "Fri" in when_text) and "6:00 PM" in when_text:
            class_name = card.find_element(By.TAG_NAME, "h3").text
            print(f"  ✓ Verified: {class_name}")
            verified_count += 1

    except NoSuchElementException:
        pass

# Simple comparison
print(f"\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_count} bookings")

if total_booked == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")
#
# # Print summary
# print("\n--- BOOKING SUMMARY ---")
# print(f"Classes booked: {booked_classes_count}")
# print(f"Waitlists joined: {waitlisted_classes_count}")
# print(f"Already booked/waitlisted: {already_booked_count}")
# print(f"Total Tuesday 6pm classes processed: {booked_classes_count + waitlisted_classes_count + already_booked_count}")

# Print detailed class list
print("\n--- DETAILED CLASS LIST ---")
for class_detail in processed_classes:
    print(f"  • {class_detail}")

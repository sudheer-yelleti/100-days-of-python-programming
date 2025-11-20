import os
import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TINDER_URL = "https://www.tinder.com/"


def init_driver():
    chrome_opts = webdriver.EdgeOptions()
    chrome_opts.add_experimental_option("detach", True)
    profile_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_opts.add_argument(f"user-data-dir={profile_dir}")

    driver = webdriver.Edge(options=chrome_opts)
    driver.maximize_window()
    return driver


def wait_for_new_window_and_switch(driver, old_handles, timeout=10):
    """Wait for new window handle to appear and switch to it. Return True if switched."""
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(lambda d: len(d.window_handles) > len(old_handles))
    except Exception:
        return False
    new_handles = [h for h in driver.window_handles if h not in old_handles]
    if not new_handles:
        return False
    driver.switch_to.window(new_handles[0])
    return True


browser = init_driver()
browser.get(TINDER_URL)
wait = WebDriverWait(browser, 15)

# open login modal
login_anchor = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//div[text()='Log in']]")))
login_anchor.click()


# Strategy 1: Try to find a provider button in the main DOM (no iframe)
def try_click_provider_in_main_dom(driver):
    candidates = [
        # common textual matches
        "//button[contains(., 'Continue with Google') or contains(., 'Continue with Google')]",
        "//div[contains(., 'Continue with Google') and (self::button or self::div or self::a)]",
        # alternate text variants
        "//*[contains(text(),'Continue with Google') or contains(text(),'Continue with google')]",
        "//*[contains(text(),'Log in with Google') or contains(text(),'Sign in with Google')]",
        # generic social provider icons/buttons - Tinder sometimes uses data-testid attributes
        "//button[contains(@aria-label,'Sign in with Google')]",
        "//div[@role='button' and .//img and contains(., 'Google')]",
    ]
    for xp in candidates:
        try:
            el = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xp)))
            print("Clicked provider via main DOM xpath:", xp)
            old_handles = driver.window_handles.copy()
            el.click()
            if wait_for_new_window_and_switch(driver, old_handles, timeout=8):
                print("Switched to new popup window (main DOM click).")
                return True
            else:
                print("No new window after main DOM click.")
                # continue trying other strategies
        except Exception:
            continue
    return False


if try_click_provider_in_main_dom(browser):
    # we are now in popup window
    print("Popup should be open and switched to.")
    # you can interact with the popup here
else:
    print("Main DOM click did not open popup. Trying iframes...")

    # Strategy 2: Iterate iframes and try to click a button inside them
    time.sleep(1)
    iframes = browser.find_elements(By.TAG_NAME, "iframe")
    print("Iframes found:", len(iframes))
    clicked = False
    for idx, iframe in enumerate(iframes):
        src = iframe.get_attribute("src")
        print(f"[{idx}] iframe src: {src}")
        try:
            browser.switch_to.frame(iframe)
            # try to click inside iframe
            try:
                # Use general button queries inside iframe
                btn = WebDriverWait(browser, 2).until(EC.element_to_be_clickable(
                    (By.XPATH,
                     "//*[contains(text(),'Continue with Google') or contains(., 'Sign in with Google') or contains(., 'Continue with Google')]")
                ))
                old_handles = browser.window_handles.copy()
                ActionChains(browser).move_to_element(btn).click(btn).perform()
                print("Clicked inside iframe index", idx)
                browser.switch_to.default_content()
                if wait_for_new_window_and_switch(browser, old_handles, timeout=8):
                    print("Switched to popup opened by iframe click.")
                    clicked = True
                    break
                else:
                    print("No new window after iframe click (index {})".format(idx))
            except Exception:
                # no matching button inside this iframe
                browser.switch_to.default_content()
        except WebDriverException as e:
            # likely a cross-origin iframe that Selenium can't access
            print("Could not switch to iframe (likely cross-origin).", e)
            browser.switch_to.default_content()
            continue

    if not clicked:
        print("Could not click button inside any accessible iframe.")
        # Strategy 3 (fallback): open the accounts iframe src in a NEW WINDOW via JS (window.open)
        # Often accounts.google.com or a google iframe src exists; opening in a new window simulates the popup
        google_src = None
        for iframe in iframes:
            src = iframe.get_attribute("src")
            if src and ("accounts.google.com" in src or "google" in src or "gsi/iframe" in src):
                google_src = src
                break

        if google_src:
            print("Found google iframe src - opening in new window via window.open() as fallback.")
            old_handles = browser.window_handles.copy()
            # open in a new window/tab (this more closely matches a popup than driver.get())
            browser.execute_script("window.open(arguments[0], '_blank', 'noopener');", google_src)
            if wait_for_new_window_and_switch(browser, old_handles, timeout=8):
                print("Switched to new window opened from iframe src.")
            else:
                print("Fallback open did not create a new window (blocked?).")
        else:
            print("No google iframe src found to use as fallback. Manual interaction required.")

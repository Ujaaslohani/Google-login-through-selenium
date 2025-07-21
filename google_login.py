import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CREDENTIALS (⚠️ Use with caution) ---
EMAIL = "youremail@gmail.com"
PASSWORD = "password"

# --- Setup WebDriver ---
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Clean console logs

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# --- Login Logic ---
def login_to_google(driver):
    driver.get("https://accounts.google.com/")
    print("Opening Google login page...")

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )

        print("Typing email...")
        for ch in EMAIL:
            email_input.send_keys(ch)
            time.sleep(0.1)

        driver.find_element(By.ID, "identifierNext").click()
        time.sleep(3)

        print("Typing password...")
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )

        for ch in PASSWORD:
            password_input.send_keys(ch)
            time.sleep(0.1)

        driver.find_element(By.ID, "passwordNext").click()

        print("Waiting for potential CAPTCHA or OTP (20 sec)...")
        time.sleep(20)

        return True

    except TimeoutException:
        print("Login form took too long to load.")
        return False

# --- Navigate to My Account ---
def go_to_my_account(driver):
    print("Navigating to Google My Account page...")
    driver.get("https://myaccount.google.com/")
    WebDriverWait(driver, 15).until(EC.title_contains("Google Account"))
    print("You are now on your Google Account dashboard.")

# --- Main ---
if __name__ == "__main__":
    driver = setup_driver()

    if login_to_google(driver):
        go_to_my_account(driver)
    else:
        print("Login failed.")

    input("Press Enter to quit...")
    driver.quit()

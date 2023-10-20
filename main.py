from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


LINKEDLN_URL = "https://www.linkedin.com/home"
EMAIL = input("Enter your email id: ")
PASSWORD = input("Enter your linkedln password: ")
PHONE = input("Enter your phone number: ")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(url=LINKEDLN_URL)


def abort():
    """Cancels the current application. Also used to close the dialog box when the application is submitted."""
    close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
    close_button.click()
    time.sleep(2)
    discard_button = driver.find_elements(
        By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn"
    )[0]
    discard_button.click()


def login():
    """Login into the linkedln website"""
    # enter email and then enter password
    enter_email = driver.find_element(By.NAME, "session_key")
    enter_email.send_keys(EMAIL)
    enter_email.send_keys(Keys.ENTER)

    enter_password = driver.find_element(By.NAME, "session_password")
    enter_password.send_keys(PASSWORD)

    # press enter to login
    enter_password.send_keys(Keys.ENTER)


time.sleep(5)

login()

# searches for "Python Developer" in India
JOB_URL = "https://www.linkedin.com/jobs/search/?currentJobId=3715291776&f_LF=f_AL&geoId=102713980&keywords=python%20developer&location=India&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON"

jobs_applied_now = 0

time.sleep(1)

driver.get(JOB_URL)

time.sleep(3)

# get all the job listings
all_listings = driver.find_elements(
    by=By.CSS_SELECTOR, value=".job-card-container--clickable"
)

for listing in all_listings:
    listing.click()
    time.sleep(3)

    try:
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        apply_button.click()
        time.sleep(3)

        phone = driver.find_element(By.CSS_SELECTOR, "input[id*=phoneNumber]")
        phone.send_keys(PHONE)

        submit_button = driver.find_element(By.CSS_SELECTOR, "footer div button")
        print(submit_button.get_attribute("aria-label"))

        if submit_button.get_attribute("aria-label") == "Continue to next step":
            # "next" button is showing hence a multi step application
            abort()
            print("Complex application, skipped.")
            continue
        else:
            time.sleep(5)
            submit_button.click()
            jobs_applied_now += 1
            print("Successfully applied")
            abort()

    # If already applied to job or job is no longer accepting applications, then skip.
    except NoSuchElementException:
        print("No application button, skipped.")
        abort()
        continue

time.sleep(5)
driver.quit()

print(f"Jobs applied today: {jobs_applied_now}")

import os
import pytest
import time
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import pyautogui
import allure
from dataconfig import generate_unique_data
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

@pytest.fixture(scope="module")
def driver():
    # Initialize the Chrome driver with options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()
    print("Driver quit in fixture")

def wait_for_page_load(driver):
    WebDriverWait(driver, 15).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

def read_input_values():
    # Generate unique data using the function from dataconfig.py
    config = generate_unique_data()
    return config

@allure.step("Logout")
def test_login_out(driver):
    try:
        # Wait for the profile button and click it
        Profile_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='avatar']"))
        )
        # Scroll into view and click using JavaScript to avoid interception
        driver.execute_script("arguments[0].scrollIntoView(true);", Profile_locator)
        driver.execute_script("arguments[0].click();", Profile_locator)
        print("Click Profile")
        time.sleep(5)

        # Wait for the Logout button and click it
        Logout_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Logout']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", Logout_locator)
        driver.execute_script("arguments[0].click();", Logout_locator)
        print("Logout Click Button")
        time.sleep(5)

        # Confirm logout by clicking the final Logout button
        Logout_confirm_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Logout']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", Logout_confirm_locator)
        driver.execute_script("arguments[0].click();", Logout_confirm_locator)

        # Wait for logout to be successful
        Logout_successful = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@id='prompt-logo-center']"))
        )
        print(f"Logout successful: element found - {Logout_successful}")
        print("Logout successful")

    except (NoSuchElementException, TimeoutException):
        print("Logout failed")
    except TimeoutException as e:
        print("Logout failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("Logout_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Logout failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("Logout_element_error.png")
        raise
    except Exception as e:
        print("Logout failed")
        print(f"An unexpected error occurred during Add Users: {e}")
        driver.save_screenshot("Logout_error.png")
        raise
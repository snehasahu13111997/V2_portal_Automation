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



def wait_for_page_load(driver):
    WebDriverWait(driver, 15).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

def read_input_values():
    # Generate unique data using the function from dataconfig.py
    config = generate_unique_data()
    return config
@allure.step("Invalid user Logging in to the portal")
def Driver_launched(driver, invalid_username, invalid_password, Uat_Portal):
    try:
        driver.get(Uat_Portal)
        time.sleep(5)
        print("Driver launched")
        wait_for_page_load(driver)
        print("Wait for page load working fine")

        Invalid_username_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'username')]"))
        )
        print("Invalid username field located")
        Invalid_username_locator.send_keys(invalid_username)

        Invalid_password_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'password')]"))
        )
        print("Invalid password field located")
        Invalid_password_locator.send_keys(invalid_password)

        login_locator = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][contains(.,'Login')]"))
        )
        print("Login button found")

        login_locator.send_keys(Keys.RETURN)
        time.sleep(5)

        Clear_username_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[contains(@aria-invalid,'true')])[1]"))
        )
        print("Clearing invalid username field")
        Clear_username_locator.clear()

        Clear_password_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@aria-invalid='true'])[2]"))
        )
        print("Clearing invalid password field")
        Clear_password_locator.clear()
        time.sleep(10)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Sanas Portal')]"))
        )


    except (NoSuchElementException, TimeoutException):
        print("Login failed as expected: Invalid username or password")

    except TimeoutException as e:
        print("Login failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("login_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Login failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("login_element_error.png")
        raise
    except Exception as e:
        print("Login failed")
        print(f"An unexpected error occurred during login: {e}")
        driver.save_screenshot("login_error.png")
        raise



@allure.step("Logging in to the portal")
def login(driver, username, password):
    try:
        wait_for_page_load(driver)
        print("Wait for page load working fine")

        username_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'username')]"))
        )
        print("Username locator found")
        username_locator.send_keys(username)

        password_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'password')]"))
        )
        print("Password locator found")
        password_locator.send_keys(password)

        login_locator = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][contains(.,'Login')]"))
        )
        print("Login button found")
        login_locator.send_keys(Keys.RETURN)
        time.sleep(5)
        login_successful = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Sanas Portal')]"))
        )
        print(f"Login successful: element found - {login_successful}")


    except (NoSuchElementException, TimeoutException):
        print("Login failed : Invalid username or password")

    except TimeoutException as e:
        print("Login failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("login_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Login failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("login_element_error.png")
        raise
    except Exception as e:
        print("Login failed")
        print(f"An unexpected error occurred during login: {e}")
        driver.save_screenshot("login_error.png")
        raise

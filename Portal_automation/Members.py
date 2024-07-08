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

@allure.step("Create invalid Members")
def create_invalid_members(driver,invalid_Email):
        try:
            members_locator = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "(//div[@class='flex-fill'][contains(.,'Members')])[1]"))
            )
            members_locator.click()
            time.sleep(10)

            # Invite user
            inviteUser_locator = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'person_addInvite users')]"))
            )
            inviteUser_locator.click()
            time.sleep(10)
            print("Invite user locator")

            # Add email
            addemail_locator = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "(//input[contains(@type,'text')])[2]"))
            )
            addemail_locator.click()
            addemail_locator.send_keys(invalid_Email)
            time.sleep(5)
            print("Add email")

            # Send invites
            sendinvite_locator = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Send invites')]"))
            )
            sendinvite_locator.send_keys(Keys.RETURN)
            print("'Send invites' button clicked")

            Send_invites = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//div[contains(.,'errorAt least one user should be added!')])[7]"))
            )
            print(f"At least one user should be added!: element found - {Send_invites}")

            print("Closed modal")
            time.sleep(3)
            Close_locator_members = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='close']"))
            )
            Close_locator_members.click()
            print("'Close' button clicked, members page closed")
            time.sleep(5)

        except (NoSuchElementException, TimeoutException):
            print("invalid Members failed")

        except TimeoutException as e:
            print("failed due to a timeout.")
            print(f"TimeoutException: {e}")
            driver.save_screenshot("invalid_Members_timeout_error.png")
            raise
        except NoSuchElementException as e:
            print("failed due to an element not being found.")
            print(f"NoSuchElementException: {e}")
            driver.save_screenshot("invalid_Members_element_error.png")
            raise
        except Exception as e:
            print("failed")
            print(f"An unexpected error occurred during login: {e}")
            driver.save_screenshot("invalid_Members_error.png")
            raise


@allure.step("Create Members")
def create_members(driver, Email):
    try:
        members_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[@class='flex-fill'][contains(.,'Members')])[1]"))
        )
        members_locator.click()
        time.sleep(10)

        # Invite user
        inviteUser_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'person_addInvite users')]"))
        )
        inviteUser_locator.click()
        time.sleep(10)
        print("Invite user")

        # Add email
        addemail_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[contains(@type,'text')])[2]"))
        )
        addemail_locator.click()
        addemail_locator.send_keys(Email)
        time.sleep(5)
        print("Add email")

        # Click on add button
        addbutton_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Add')]"))
        )
        addbutton_locator.click()
        time.sleep(5)

        # Send invites
        sendinvite_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Send invites')]"))
        )
        sendinvite_locator.send_keys(Keys.RETURN)

        time.sleep(5)
        invites_Successfully = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[contains(.,'User invites sent successfully!')])[3]"))
        )
        print(f"Members invites Successfully: element found - {invites_Successfully}")
        time.sleep(5)

    except (NoSuchElementException, TimeoutException):
        print("invalid Members failed")

    except TimeoutException as e:
        print("failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("Members_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("Members_element_error.png")
        raise
    except Exception as e:
        print("Members failed")
        print(f"An unexpected error occurred during login: {e}")
        driver.save_screenshot("Members_error.png")
        raise

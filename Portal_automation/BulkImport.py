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


@allure.step("Bulk import inside the selected Team")
def Bulk_import_CSV(driver, CSV):
    try:
        Team_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Teams']"))
        )
        Team_locator.click()
        print("Click teams button")
        time.sleep(5)
        Upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'flex flex-middle gap-small flex-center btn white normal')]"))
        )
        Upload_button.click()
        print("Click on import button")
        time.sleep(5)
        Bulk_Add = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Add']"))
        )
        Bulk_Add.click()
        print("Click on the Bulk Add button")
        time.sleep(5)
        file_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Select .csv file')]"))
        )
        file_input.click()
        time.sleep(2)
        pyautogui.write(CSV)
        pyautogui.press('Enter')
        time.sleep(5)
        print("CSV File selected")

        Bulk_Upload = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Upload')]"))
        )
        Bulk_Upload.click()
        print("Click upload button to add user")

        Confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Confirm')]"))
        )
        Confirm_button.send_keys(Keys.RETURN)
        print("Click confirm button")

        Closed_locator = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Close')]"))
        )
        Closed_locator.click()
        print("Bulk import successfully completed")

    except (NoSuchElementException, TimeoutException):
        print("Bulk import failed")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Bulk import failed: {e}")
        driver.save_screenshot("Bulk_import_error.png")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during Bulk import: {e}")
        driver.save_screenshot("Bulk_import_unexpected_error.png")
        raise


    except TimeoutException as e:
        print("Bulk_import due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("Bulk_import_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Bulk_import failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("Bulk_import_element_error.png")
        raise

@allure.step("invalid Bulk import inside the selected Team")
def Bulk_import_CSVinvalid(driver, invalid_CSV):
    try:
        Team_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Teams']"))
        )
        Team_locator.click()
        print("Click teams button")
        time.sleep(5)
        Upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'flex flex-middle gap-small flex-center btn white normal')]"))
        )
        Upload_button.click()
        print("Click on import button")
        time.sleep(5)
        Bulk_Add = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Add']"))
        )
        Bulk_Add.click()
        print("Click on the Bulk Add button")
        time.sleep(5)
        file_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Select .csv file')]"))
        )
        file_input.click()
        time.sleep(2)
        pyautogui.write(invalid_CSV)
        pyautogui.press('Enter')
        time.sleep(5)
        print("CSV File selected")

        Bulk_Upload = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Upload')]"))
        )
        Bulk_Upload.click()
        print("Click upload button to add user")

        Closed_locator = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//span[contains(.,'close')])[1]"))
        )
        Closed_locator.click()
        print("Bulk import : invalid CSV file")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Bulk import failed: {e}")
        driver.save_screenshot("Bulk_import_error.png")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during Bulk import: {e}")
        driver.save_screenshot("Bulk_import_unexpected_error.png")
        raise

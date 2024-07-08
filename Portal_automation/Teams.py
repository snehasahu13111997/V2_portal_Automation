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

@allure.step("Create team inside the selected workspace")
def create_team(driver, TeamName, NewUser, UserId):
    try:
        Team_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Teams']"))
        )
        Team_locator.click()
        print("Click teams button")
        time.sleep(5)

        # Click on create team button
        createTeam_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'group_addCreate team')]"))
        )
        createTeam_locator.click()
        print("Click Create team button")
        time.sleep(5)

        # Add Team name
        addTeamName_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@class='form-input'])[1]"))
        )
        addTeamName_locator.click()
        addTeamName_locator.send_keys(TeamName)
        print("Add Team Name")
        time.sleep(5)

        # add user inside team
        # enter name
        NameUser_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@type='text'])[3]"))
        )
        NameUser_locator.click()
        NameUser_locator.send_keys(NewUser)
        print("Add User")
        time.sleep(5)

        # enter userid
        UserId_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@type='text'])[4]"))
        )
        UserId_locator.click()
        UserId_locator.send_keys(UserId)
        print("Add User Id")
        time.sleep(5)

        # Click add button to add user
        Adduser_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Add')]"))
        )
        Adduser_locator.click()
        print("Click add button")

        time.sleep(5)

        # Click on create team finally
        createTeamFinalButton_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//button[contains(.,'Create team')])[2]"))
        )
        createTeamFinalButton_locator.send_keys(Keys.RETURN)

        Team_created_successfully = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[contains(.,'Team created successfully!')])[3]"))
        )
        print(f"Login successful: element found - {Team_created_successfully}")
        print("Team created successfully")
        time.sleep(10)
        close_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='close']"))
        )
        close_locator.click()
        print("close created team")
    except (NoSuchElementException, TimeoutException):
        print("Failed : Team created")

    except TimeoutException as e:
        print("Team created failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("Team_created_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Team created failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("Team_created_NoSuchElementException.png")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("Team_created_error.png")
        raise


@allure.step("Create Invalid User inside team")
def test_Invalid_UserId(driver, Invalid_UserName, Invalid_UserId):
    try:
        Team_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Teams']"))
        )
        Team_locator.click()
        print("Click teams button")
        time.sleep(5)

        Default_Team_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Default TeamDefault')])[6]"))
        )
        Default_Team_locator.click()
        print("Default_Team Click")
        Addusers_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='flex flex-middle gap-small flex-center btn primary normal']"))
        )
        Addusers_locator.click()

        # enter userid
        Invalid_UserId_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(// input[contains( @ maxlength, '32')])[2]"))
        )
        Invalid_UserId_locator.send_keys(Invalid_UserId)
        print("Enter UserID")

        # enter User Name
        Invalid_UserName_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@type='text'])[2]"))
        )
        Invalid_UserName_locator.send_keys(Invalid_UserName)
        print("Enter User Name")

        UserId_Button_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//button[contains(.,'Add users')])[2]"))
        )
        UserId_Button_locator.send_keys(Keys.RETURN)

        print("Click Button")
        Add_Users_successful = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[contains(.,'errorAdd at least one user!')])[7]"))
        )
        print(f"errorAdd at least one user!: element found - {Add_Users_successful}")
        time.sleep(5)
        Cloed_adduser_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//span[contains(@class,'material-symbols-rounded')])[23]"))
        )
        Cloed_adduser_locator.click()

    except (NoSuchElementException, TimeoutException):
        print("Add Users failed ")

    except TimeoutException as e:
        print("Add Users failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("Add_Users_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Add Users failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("Add_Users_element_error.png")
        raise
    except Exception as e:
        print("Add Users failed")
        print(f"An unexpected error occurred during Add Users: {e}")
        driver.save_screenshot("Add_Users_error.png")
        raise

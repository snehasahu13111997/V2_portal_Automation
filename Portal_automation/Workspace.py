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
@allure.step("workspace_already_exists")
def workspace_already_exists(driver, Enterprise_exists, BPO_exists, location_exists, seats_exists):
    try:
        print("Locating 'Workspaces' button")
        workspaces_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Workspaces')])[4]"))
        )
        workspaces_locator.click()
        time.sleep(2)

        print("Locating 'Create workspace' button")
        create_workspace_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'domain_addCreate workspace')]"))
        )
        create_workspace_locator.click()

        print("Waiting for 'Create workspace' popup")
        create_workspace_popup_heading_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//h5[contains(.,'Create workspace')]"))
        )

        print("Entering enterprise details")
        enterprise_placeholder_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter enterprise']"))
        )
        enterprise_placeholder_locator.send_keys(Enterprise_exists)
        time.sleep(1)

        print("Entering BPO details")
        bpo_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@tabindex,'2')]"))
        )
        bpo_locator.click()
        time.sleep(1)
        bpo_locator.send_keys(BPO_exists)

        print("Entering location details")
        location_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@tabindex,'3')]"))
        )
        location_locator.send_keys(location_exists)
        time.sleep(5)

        print("Selecting 'IND'")
        IND_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='flex gap-small flex-middle flex-center'][normalize-space()='IND']"))
        )
        IND_locator.click()
        time.sleep(5)

        print("Selecting 'PHL'")
        PHL_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='flex gap-small flex-middle flex-center'][normalize-space()='PHL']"))
        )
        PHL_locator.click()
        time.sleep(5)

        print("Selecting 'Accent translation'")
        accentTranslation_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Accent Translation')])[9]"))
        )
        accentTranslation_locator.click()
        time.sleep(5)

        print("Selecting 'Noise Cancellation'")
        voiceEnhancement_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Noise Cancellation')])[9]"))
        )
        voiceEnhancement_locator.click()
        time.sleep(3)

        print("Entering seat details")
        seats_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@tabindex,'8')]"))
        )
        seats_locator.send_keys(seats_exists)
        time.sleep(1)

        print("Creating workspace and sending invite")
        createWorkspace_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Create workspace & send invite')]"))
        )
        createWorkspace_locator.send_keys(Keys.RETURN)


        workspace_already_exists = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'flex-fill')])[12]"))
        )
        print(f"workspace already exists: element found - {workspace_already_exists}")
        time.sleep(5)
        print("Locating 'Close' element")
        Close_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='material-symbols-rounded'][contains(.,'close')]"))
        )
        Close_locator.click()
        print("Closed Tab")
        time.sleep(3)


    except (NoSuchElementException, TimeoutException):
        print("Failed : workspace_already_exists")

    except TimeoutException as e:
        print("Login failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("workspace_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Login failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("create_workspace_NoSuchElementException.png")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("create_workspace_error.png")
        raise


@allure.step("Create workspace")
def create_workspace(driver, Enterprise, BPO, location, seats):
    try:
        print("Locating 'Workspaces' button")
        workspaces_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Workspaces')])[4]"))
        )
        workspaces_locator.click()
        time.sleep(5)

        print("Locating 'Create workspace' button")
        create_workspace_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'domain_addCreate workspace')]"))
        )
        create_workspace_locator.click()

        print("Waiting for 'Create workspace' popup")
        create_workspace_popup_heading_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//h5[contains(.,'Create workspace')]"))
        )

        print("Entering enterprise details")
        enterprise_placeholder_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter enterprise']"))
        )
        enterprise_placeholder_locator.send_keys(Enterprise)
        time.sleep(5)

        print("Entering BPO details")
        bpo_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@tabindex,'2')]"))
        )
        bpo_locator.click()
        time.sleep(5)
        bpo_locator.send_keys(BPO)

        print("Entering location details")
        location_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@tabindex,'3')]"))
        )
        location_locator.send_keys(location)
        time.sleep(5)

        print("Selecting 'IND'")
        IND_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='flex gap-small flex-middle flex-center'][normalize-space()='IND']"))
        )
        IND_locator.click()
        time.sleep(5)

        print("Selecting 'PHL'")
        PHL_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='flex gap-small flex-middle flex-center'][normalize-space()='PHL']"))
        )
        PHL_locator.click()
        time.sleep(5)

        print("Selecting 'Accent translation'")
        accentTranslation_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Accent Translation')])[9]"))
        )
        accentTranslation_locator.click()
        time.sleep(5)

        print("Selecting 'Noise Cancellation'")
        voiceEnhancement_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "(//div[contains(.,'Noise Cancellation')])[9]"))
        )
        voiceEnhancement_locator.click()
        time.sleep(3)


        print("Entering seat details")
        seats_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@tabindex,'8')]"))
        )
        seats_locator.send_keys(seats)
        time.sleep(5)

        print("Creating workspace and sending invite")
        createWorkspace_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Create workspace & send invite')]"))
        )
        createWorkspace_locator.send_keys(Keys.RETURN)

        createWorkspace_successful = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'flex-fill')])[11]"))
        )
        print(f"Create Workspace Successful: element found - {createWorkspace_successful}")
        time.sleep(5)

        print("Selecting workspace dropdown")
        workspaceDropdown_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[@class='workspace-name']"))
        )
        workspaceDropdown_locator.click()
        time.sleep(5)

        print("Searching for the workspace")
        searchWorkspace_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@placeholder='Search'])[2]"))
        )
        searchWorkspace_locator.click()
        time.sleep(5)
        searchWorkspace_locator.send_keys(Enterprise)
        time.sleep(5)

        print("Selecting the searched workspace")
        selectSearchedWorkspace_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(@class,'text-caption text-sm')]"))
        )
        selectSearchedWorkspace_locator.click()
        Searched_Workspace_Successful = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[contains(@class,'flex-fill')])[11]"))
        )
        print(f"Searched Workspace Successful: element found - {Searched_Workspace_Successful}")
        time.sleep(5)

    except (NoSuchElementException, TimeoutException):
        print("Searched Workspace Failed")

    except TimeoutException as e:
        print("Login failed due to a timeout.")
        print(f"TimeoutException: {e}")
        driver.save_screenshot("Create_workspace_timeout_error.png")
        raise
    except NoSuchElementException as e:
        print("Login failed due to an element not being found.")
        print(f"NoSuchElementException: {e}")
        driver.save_screenshot("Create_workspace_element_error.png")
        raise
    except Exception as e:
        print("Create workspace failed")
        print(f"An unexpected error occurred during login: {e}")
        driver.save_screenshot("Create_workspace_error.png")
        raise


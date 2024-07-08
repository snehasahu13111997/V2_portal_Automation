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
import Members
import logout
import login
import Teams
import BulkImport

import Workspace

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


def test_smoke_suite(driver):
    config = read_input_values()
    login.Driver_launched(driver, config['invalid_username'], config['invalid_password'], config['Uat_Portal'])
    login.login(driver, config['username'], config['password'])
    Workspace.workspace_already_exists(driver, config['Enterprise_exists'], config['BPO_exists'], config['location_exists'], config['seats_exists'])
    Workspace.create_workspace(driver, config['Enterprise'], config['BPO'], config['location'], config['seats'])
    Members.create_invalid_members(driver, config['invalid_Email'])
    Members.create_members(driver, config['Email'])
    Teams.create_team(driver, config['TeamName'], config['NewUser'], config['UserId'])
    Teams.test_Invalid_UserId(driver, config['Invalid_UserName'], config['Invalid_UserId'])
    logout.test_login_out(driver)


def test_sanity_suite(driver):
    config = read_input_values()
    login.Driver_launched(driver, config['invalid_username'], config['invalid_password'], config['Uat_Portal'])
    login.login(driver, config['username'], config['password'])
    Workspace.workspace_already_exists(driver, config['Enterprise_exists'], config['BPO_exists'], config['location_exists'], config['seats_exists'])
    Workspace.create_workspace(driver, config['Enterprise'], config['BPO'], config['location'], config['seats'])
    Members.create_invalid_members(driver, config['invalid_Email'])
    Members.create_members(driver, config['Email'])
    Teams.create_team(driver, config['TeamName'], config['NewUser'], config['UserId'])
    Teams.test_Invalid_UserId(driver, config['Invalid_UserName'], config['Invalid_UserId'])
    BulkImport.Bulk_import_CSV(driver, config['CSV'])
    BulkImport.Bulk_import_CSVinvalid(driver, config['invalid_CSV'])
    logout.test_login_out(driver)

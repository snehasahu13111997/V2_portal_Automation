import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import pyautogui
import json
import allure

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

def read_input_values(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

@allure.step("Logging in to the portal")
def login(driver, username, password, Uat_Portal):
    try:
        driver.get(Uat_Portal)
        time.sleep(5)
        print("Driver launched")
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
        login_locator.click()
        time.sleep(10)
    except Exception as e:
        print(f"An error occurred during login: {e}")
        driver.save_screenshot("login_error.png")
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
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'IND')])[9]"))
        )
        IND_locator.click()
        time.sleep(5)

        print("Selecting 'PHL'")
        PHL_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'PHL')])[9]"))
        )
        PHL_locator.click()
        time.sleep(5)

        print("Selecting 'Accent translation'")
        accentTranslation_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Accent translation')])[9]"))
        )
        accentTranslation_locator.click()
        time.sleep(5)

        print("Selecting 'Voice enhancement'")
        voiceEnhancement_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Voice enhancement')])[9]"))
        )
        voiceEnhancement_locator.click()
        time.sleep(5)

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
        createWorkspace_locator.click()
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
        time.sleep(10)

        print("Selecting the searched workspace")
        selectSearchedWorkspace_locator = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(@class,'text-caption text-sm')]"))
        )
        selectSearchedWorkspace_locator.click()
        time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("create_workspace_error.png")
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
        sendinvite_locator.click()
        print("Send invites")
        time.sleep(5)
        print("Members invites Successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("create_members_error.png")
        raise

@allure.step("Create team inside the selected workspace")
def create_team(driver, TeamName, NewUser, UserId, Email):
    try:
        Team_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[@class='flex-fill'][contains(.,'Teams')])[1]"))
        )
        Team_locator.click()
        time.sleep(5)

        # Click on create team button
        createTeam_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'group_addCreate team')]"))
        )
        createTeam_locator.click()
        time.sleep(10)
        print("Create team")

        # Enter team name
        teamName_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@type='text'])[2]"))
        )
        teamName_locator.click()
        teamName_locator.send_keys(TeamName)
        time.sleep(5)
        print("Enter team name")

        # Add supervisor
        addSupervisor_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        addSupervisor_locator.click()
        addSupervisor_locator.send_keys(Email)
        time.sleep(5)
        print("Add supervisor")

        # Add user inside team
        # Enter name
        NameUser_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@type='text'])[3]"))
        )
        NameUser_locator.click()
        NameUser_locator.send_keys(NewUser)
        time.sleep(5)
        print("Enter Username")

        # Enter user ID
        UserId_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@type='text'])[4]"))
        )
        UserId_locator.click()
        UserId_locator.send_keys(UserId)
        time.sleep(5)
        print("Enter UserID")

        # Click add button to add user
        Adduser_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Add')]"))
        )
        Adduser_locator.click()
        time.sleep(5)

        # Click on create team finally
        createTeamFinalButton_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//button[contains(.,'Create team')])[2]"))
        )
        createTeamFinalButton_locator.click()
        time.sleep(10)
        print("Create team finally")

        # Click close button
        Closed_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Close')]"))
        )
        Closed_locator.click()
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("create_team_error.png")
        raise

@allure.step("Bulk import inside the selected Team")
def Bulk_import(driver, CSV):
    try:
        upload_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'file_saveBulk import')]"))
        )
        upload_button.click()
        time.sleep(5)

        # Click on the 'Bulk Add' button
        Bulk_Add = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//div[contains(.,'Add')])[8]"))
        )
        Bulk_Add.click()
        time.sleep(8)
        print("Click on the Bulk Add button")
        # Simulate click on the file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Select .csv file')]"))
        )
        file_input.click()
        time.sleep(2)  # Add a small delay to ensure the file dialog opens

        # Use pyautogui to interact with the file dialog
        pyautogui.write(CSV)
        pyautogui.press('enter')
        print("Select your CSV File")
        # Wait for some time for the file to be uploaded
        time.sleep(5)
        Bulk_Upload = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Upload')]"))
        )
        Bulk_Upload.click()
        print("Click add button to add user")
        time.sleep(5)
        Confirm_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Confirm')]"))
        )
        Confirm_button.click()
        time.sleep(3)
        print("Click add Confirm")
        # Click add button to add user
        Closed_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(.,'Close')]"))
        )
        Closed_locator.click()
        time.sleep(10)
        print("Bulk import Successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("Bulk_Upload_error.png")
        raise


@allure.feature('Login Feature')
@allure.story('Valid Login')
def test_Login(driver):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    inputData = read_input_values(config_path)
    username = inputData['username']
    password = inputData['password']
    Uat_Portal = inputData['Uat_Portal']
    login(driver, username, password, Uat_Portal)

@allure.feature('Workspace Feature')
@allure.story('Create and Select Workspace')
def test_Workspace(driver):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    inputData = read_input_values(config_path)
    Enterprise = inputData['Enterprise']
    BPO = inputData['BPO']
    location = inputData['location']
    seats = inputData['seats']
    create_workspace(driver, Enterprise, BPO, location, seats)

@allure.feature('Members Feature')
@allure.story('Invites Members')
def test_Members(driver):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    inputData = read_input_values(config_path)
    Email = inputData['Email']
    create_members(driver, Email)

@allure.feature('Create team inside the selected workspace')
@allure.story('Create team')
def test_Create_Team(driver):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    inputData = read_input_values(config_path)
    Email = inputData['Email']
    TeamName = inputData['TeamName']
    NewUser = inputData['NewUser']
    UserId = inputData['UserId']
    create_team(driver, TeamName, NewUser, UserId, Email)


@allure.feature('Bulk import inside the selected Team')
@allure.story('Bulk import')
def test_Bulk_import(driver):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    inputData = read_input_values(config_path)
    CSV = inputData['CSV']

    # The correct function to call for bulk import is 'Bulk_import'
    Bulk_import(driver, CSV)

    try:
        post_login_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(.,'Sanas Portal')]"))
        )
        assert post_login_element is not None
    except Exception as e:
        print(f"An error occurred during post-login verification: {e}")
        driver.save_screenshot("post_login_error.png")
        raise



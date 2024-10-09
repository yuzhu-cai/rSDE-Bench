# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
import psutil
import shutil
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import subprocess
import sys

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid


class TestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()  # Make sure to have the ChromeDriver installed
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        # Close the web browser after tests
        self.driver.quit()

    # Login Page Tests
    def test_login_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'usernameField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'passwordField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'loginButton').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'registerLink').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'aboutLink').is_displayed())

    def test_login_functionality(self):
        driver = self.driver
        # Login process
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        # Verify that the user is redirected to the Dashboard (Assuming the page title or URL changes)
        self.assertIn("Dashboard", driver.title)
    #Registration Page Tests
    def test_registration_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'registerLink').click()
        self.assertTrue(driver.find_element(By.ID, 'regUsernameField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'regPasswordField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'registerButton').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'loginLink').is_displayed())

    def test_registration_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'registerLink').click()
        # Registration process
        driver.find_element(By.ID, 'regUsernameField').send_keys("new_user")
        driver.find_element(By.ID, 'regPasswordField').send_keys("new_password")
        driver.find_element(By.ID, 'registerButton').click()
        # Verify successful registration and redirection to dashboard
        with open(os.path.join('data', 'users.txt'), 'r') as file:
            users = file.readlines()
        exists = any("new_user|new_password" in line for line in users)
        self.assertTrue(exists)

    # Dashboard Page Tests
    def test_dashboard_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        self.assertTrue(driver.find_element(By.ID, 'projectList').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'createProjectButton').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'profileSettingsLink').is_displayed())
    def test_dashboard_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()

        # Verify user's projects from data storage
        with open('data/projects.txt') as file:
            projects = file.readlines()
        project_names = [project.split('|')[0] for project in projects]
        for project in range(len(project_names)):
            self.assertTrue(driver.find_element(By.ID, f'project_{project}').is_displayed())
        driver.find_element(By.ID, 'profileSettingsLink').click()
        self.assertIn("Profile Settings", driver.title)
    #Create Project Page Tests
    def test_create_project_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        driver.find_element(By.ID, 'createProjectButton').click()
        self.assertTrue(driver.find_element(By.ID, 'projectNameField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'projectDescriptionField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'collaboratorsField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'createButton').is_displayed())
    def test_create_project_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        driver.find_element(By.ID, 'createProjectButton').click()
        # Create a project
        driver.find_element(By.ID, 'projectNameField').send_keys("New_Project")
        driver.find_element(By.ID, 'projectDescriptionField').send_keys("Description of new project")
        driver.find_element(By.ID, 'collaboratorsField').send_keys("jane_smith")
        driver.find_element(By.ID, 'createButton').click()
        # Verify the new project in data storage
        with open('data/projects.txt') as file:
            projects = file.readlines()
        self.assertIn("New_Project|Description of new project|jane_smith\n", projects)
    # Project Details Page Tests
    def test_project_details_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        driver.find_element(By.ID, 'project_0').click()  # Assuming project_0 is the first project
        self.assertTrue(driver.find_element(By.ID, 'projectDetailView').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'collaboratorsList').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'musicLinkInputField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'uploadFileButton').is_displayed())

    def test_project_details_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        driver.find_element(By.ID, 'project_0').click()  # Click on the first project
        # Upload a file
        driver.find_element(By.ID, 'musicLinkInputField').send_keys("www.example_3.com")
        driver.find_element(By.ID, 'uploadFileButton').click()
        # Verify that file is uploaded (Assuming it is reflected in uploadedFilesDisplay somehow)
        self.assertTrue(driver.find_element(By.ID, 'uploadStatusMessage').is_displayed())

    # Profile Settings Page Tests
    def test_profile_settings_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        driver.find_element(By.ID, 'profileSettingsLink').click()
        self.assertTrue(driver.find_element(By.ID, 'updateUsernameField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'updatePasswordField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'updateButton').is_displayed())

    def test_profile_settings_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'usernameField').send_keys("john_doe")
        driver.find_element(By.ID, 'passwordField').send_keys("password123")
        driver.find_element(By.ID, 'loginButton').click()
        driver.find_element(By.ID, 'profileSettingsLink').click()
        # Update profile
        driver.find_element(By.ID, 'updateUsernameField').send_keys("john_doe_updated")
        driver.find_element(By.ID, 'updatePasswordField').send_keys("new_password")
        driver.find_element(By.ID, 'updateButton').click()
        # Verify if updated username and password persist in user storage
        with open('data/users.txt') as file:
            users = file.readlines()
        self.assertIn("john_doe_updated|new_password\n", users)

        
    # About Page Tests
    def test_about_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'aboutLink').click()
        self.assertTrue(driver.find_element(By.ID, 'aboutContent').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'contactInfo').is_displayed())

    def test_about_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'aboutLink').click()
        self.assertEqual("About", driver.title)

class TestMusicCollaborator:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path) 
        if not os.path.exists('data'):
            shutil.copytree(f'{code_path}/data', 'data')
        else:
            shutil.rmtree('data')  
            shutil.copytree(f'{code_path}/data', 'data')
        
        self.checker = checker
        self.time = time
        self.py = path
        self.pid = get_python_pid() 

    def test_set_up(self):
        try:
            self.process = subprocess.Popen(['python', f'{self.py}'])
            time.sleep(self.time)
        except:
            return 0
        return 1
    
    def tear_down(self):
        if os.path.exists('data'):
            shutil.rmtree('data')
        self.process.terminate()

        pid = get_python_pid()
        for p in pid:
            if p not in self.pid:
                proc = psutil.Process(p)
                proc.terminate()
        
    
    def main(self):
        result = {
            'total': 15,
            'total_basic': 8,
            'total_advanced': 7,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'set_up': 0
            }
        }
        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except:
            self.tear_down()

        if result['test_cases']['set_up'] == 1:
            try :
                test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
                res = CustomTestRunner().run(test_suite)
            except:
                print("ERROR")
        self.tear_down()

        for test in res['succ']:
            test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
            result['test_cases'][test_cases] = 1
        for test in res['fail']:
            test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
            result['test_cases'][test_cases] = 0
        
        result['basic'] += 1

        for item in result['test_cases']:
            if 'elements' in item:
                result['basic'] += result['test_cases'][item]
            if 'functionality' in item:
                result['advanced'] += result['test_cases'][item]
        
        return result
        


if __name__ == '__main__':
    checker = None
    py = r'C:\Users\84495\Desktop\asie-bench\codes\gpt-4o-mini-2\MusicCollaborator\app.py'
    test = TestMusicCollaborator(checker, py)
    print(test.main())






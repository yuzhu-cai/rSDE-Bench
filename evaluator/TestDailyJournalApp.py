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
        # Initialize the webdriver and open the main page
        self.driver = webdriver.Chrome()  # Make sure ChromeDriver is installed and on PATH
        self.driver.get('http://localhost:5000')
    
    def tearDown(self):
        # Close the web driver session
        self.driver.quit()

    def login(self):
        # Simulate user login
        username = "user1"
        password = "password123"

        # Input username and password
        self.driver.find_element(By.ID, 'username_input').send_keys(username)
        self.driver.find_element(By.ID, 'password_input').send_keys(password)
        self.driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Dashboard Page has loaded by checking an element
    def test_login_elements(self):
        # Verify the presence of elements on the Login Page
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'username_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'password_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'login_button').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'register_link').is_displayed())

    def test_login_functionality(self):
        # Simulate user login
        username = "user1"
        password = "password123"

        # Input username and password
        self.driver.find_element(By.ID, 'username_input').send_keys(username)
        self.driver.find_element(By.ID, 'password_input').send_keys(password)
        self.driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Dashboard Page has loaded by checking an element
        self.assertIn("Dashboard", self.driver.title)

    def test_registration_elements(self):
        driver = self.driver
        # Navigate to Registration Page
        driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the presence of elements on the Registration Page
        self.assertTrue(driver.find_element(By.ID, 'reg_username_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'reg_password_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'register_button').is_displayed())

    def test_registration_functionality(self):
        # Simulate user registration
        self.driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the next page to load

        reg_username = "new_user"
        reg_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.ID, 'reg_username_input').send_keys(reg_username)
        self.driver.find_element(By.ID, 'reg_password_input').send_keys(reg_password)
        self.driver.find_element(By.ID, 'register_button').click()
        time.sleep(1)  # Wait for the next page to load after registration

        # Verify the user is logged in by checking for an element in the Dashboard Page
        with open(os.path.join('data', 'user_credentials.txt'), 'r') as file:
            users = file.readlines()
        exists = any("new_user|new_password" in line for line in users)
        self.assertTrue(exists)
    def test_dashboard_elements(self):
        # Simulate user login to access the Dashboard
        self.login()  # Reuse the login functionality test

        # Verify the presence of elements on the Dashboard Page
        self.assertTrue(self.driver.find_element(By.ID, 'new_entry_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'entry_list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'logout_button').is_displayed())

    def test_dashboard_functionality(self):
        # Simulate user login and then add a new journal entry
        self.login()  # Reuse the login functionality test

        # Access the New Entry page
        self.driver.find_element(By.ID, 'new_entry_button').click()
        time.sleep(1)
        self.assertIn("New Journal Entry", self.driver.title)


    def test_new_entry_elements(self):
        # Simulate user login to access New Entry Page
        self.login()  # Reuse the login functionality test

        # Navigate to New Entry Page
        self.driver.find_element(By.ID, 'new_entry_button').click()
        time.sleep(1)

        # Verify presence of elements on the New Entry Page
        self.driver.find_element(By.ID, 'entry_title_field')
        self.driver.find_element(By.ID, 'entry_content_field')
        self.driver.find_element(By.ID, 'save_entry_button')


    def test_new_entry_functionality(self):
        # Simulate user login to access New Entry Page
        self.login()  # Reuse the login functionality test

        # Navigate to New Entry Page
        self.driver.find_element(By.ID, 'new_entry_button').click()
        time.sleep(1)


        entry_title = "My New Journal Entry"
        entry_content = "This is the content of my new journal entry."

        # Fill out the new entry form
        self.driver.find_element(By.ID, 'entry_title_field').send_keys(entry_title)
        self.driver.find_element(By.ID, 'entry_content_field').send_keys(entry_content)
        self.driver.find_element(By.ID, 'save_entry_button').click()
        time.sleep(1)  # Wait for saving the entry

        with open(os.path.join('data', 'journal_entries.txt'), 'r') as file:
            tasks = file.readlines()
        task_added = any("My New Journal Entry|This is the content of my new journal entry." in line for line in tasks)
        self.assertTrue(task_added)


class TestDailyJournalApp:
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
            'total': 9,
            'total_basic': 5,
            'total_advanced': 4,
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
    py = r'D:\research\asie-bench_withweb\codes\gpt-4o-mini-0\DailyJournalApp\app.py'
    test = TestDailyJournalApp(checker, py)
    print(test.main())


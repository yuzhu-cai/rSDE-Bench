import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select 
import time
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):
    def setUp(self):
        """Set up the Selenium WebDriver before each test."""
        self.driver = webdriver.Chrome()  # You can specify the path to your WebDriver here
        self.driver.get("http://localhost:5000")  # Start from the landing page
    
    def tearDown(self):
        """Tear down the WebDriver after each test."""
        self.driver.quit()
    
    def login(self):
        self.driver.delete_all_cookies()  
        username = "john_doe"
        password = "password123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
    
    # --- Login Page Tests ---

    def test_login_elements(self):
        # Verify the essential elements in the login page are present
        login_form = self.driver.find_element(By.ID, 'login-form')
        username_input = self.driver.find_element(By.ID, 'username')
        password_input = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.ID, 'login-button')

        self.assertTrue(login_form.is_displayed())
        self.assertTrue(username_input.is_displayed())
        self.assertTrue(password_input.is_displayed())
        self.assertTrue(login_button.is_displayed())

    def test_login_functionality(self):
        # Test the login functionality with a valid user
        self.assertIn("User Login", self.driver.title)

        valid_username = 'john_doe'
        valid_password = 'password123'

        self.driver.find_element(By.ID, 'username').send_keys(valid_username)
        self.driver.find_element(By.ID, 'password').send_keys(valid_password)
        self.driver.find_element(By.ID, 'login-button').click()
        self.assertIn("Elder Care Resources Dashboard", self.driver.title)
    
    # --- Dashboard Page Tests ---

    def test_dashboard_page_elements(self):
        # After login navigate to dashboard
        self.login()
        resource_list = self.driver.find_element(By.ID, 'resource-list')
        logout_button = self.driver.find_element(By.ID, 'logout-button')
        contact_button = self.driver.find_element(By.ID, 'contact-button')

        self.assertTrue(resource_list.is_displayed())
        self.assertTrue(logout_button.is_displayed())
        self.assertTrue(contact_button.is_displayed())

    def test_dashboard_functionality(self):
        self.login()

        welcome_message = self.driver.find_element(By.ID, 'welcome-message').text
        self.assertIn("welcome", welcome_message.lower())

        resource_displayed = self.driver.find_element(By.ID, 'resource-list').text
        with open(os.path.join('data', 'resources.txt'), 'r') as resource_file:
            resources = resource_file.readlines()
        res_id = [line.split(",")[0] for line in resources]
        res_title = [line.split(",")[1] for line in resources]
        res_desc = [line.split(",")[2].strip() for line in resources]
        
        for id in res_id:
            self.assertIn(id, resource_displayed)
        for title in res_title:
            self.assertIn(title, resource_displayed)
        for desc in res_desc:
            self.assertIn(desc, resource_displayed) 
        
        self.login()
        self.driver.find_element(By.ID, 'contact-button').click()
        self.assertIn("Contact Us", self.driver.title)

            
    # --- Contact Page Tests ---

    def test_contact_page_elements(self):
        # After login navigate to contact page
        self.login()
        self.driver.find_element(By.ID, 'contact-button').click()

        contact_form = self.driver.find_element(By.ID, 'contact-form')
        contact_name_input = self.driver.find_element(By.ID, 'contact-name')
        contact_email_input = self.driver.find_element(By.ID, 'contact-email')
        contact_message_input = self.driver.find_element(By.ID, 'contact-message')
        submit_button = self.driver.find_element(By.ID, 'submit-button')

        self.assertTrue(contact_form.is_displayed())
        self.assertTrue(contact_name_input.is_displayed())
        self.assertTrue(contact_email_input.is_displayed())
        self.assertTrue(contact_message_input.is_displayed())
        self.assertTrue(submit_button.is_displayed())

    def test_contact_functionality(self):
        # Test submitting a contact form
        self.login()
        self.driver.find_element(By.ID, 'contact-button').click()

        name = "Carlla"
        email = "carlla@example.com"
        message = "Who are you?"
        
        self.driver.find_element(By.ID, 'contact-name').send_keys(name)
        self.driver.find_element(By.ID, 'contact-email').send_keys(email)
        self.driver.find_element(By.ID, 'contact-message').send_keys(message)
        self.driver.find_element(By.ID, 'submit-button').click()

        # Check if the inquiry has been recorded
        with open(os.path.join('data', 'inquiries.txt'), 'r') as inquiry_file:
            inquiries = inquiry_file.readlines()
        self.assertIn(f"{name},{email},{message}\n", inquiries)


class TestElderCareResources:
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
            'total': 7,
            'total_basic': 4,
            'total_advanced': 3,
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
    py = r'C:\Users\84495\Desktop\asie-bench\ElderCareResources-0\app.py'
    test = TestElderCareResources(checker, py)
    print(test.main())
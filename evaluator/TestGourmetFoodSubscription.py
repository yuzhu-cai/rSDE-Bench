import os
import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):

    def setUp(self):
        # Initialize the web driver (make sure to provide the proper path for your web driver)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        # Close the browser session
        self.driver.quit()

    def login(self):
        self.driver.delete_all_cookies()
        username = "john_doe"
        password = "abcd1234"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_elements(self):
        self.assertEqual(self.driver.title, "Login")
        self.driver.find_element(By.ID, "username_field")
        self.driver.find_element(By.ID, "password_field")
        self.driver.find_element(By.ID, "login_button")
        # self.driver.find_element(By.ID, "error_message")
        self.driver.find_element(By.ID, "register_link")

    def test_login_functionality(self):
        self.driver.find_element(By.ID, "username_field").send_keys("john_doe")
        self.driver.find_element(By.ID, "password_field").send_keys("abcd1234")
        self.driver.find_element(By.ID, "login_button").click()
        self.assertIn("Dashboard", self.driver.title)

        # Check if redirected to the Registration Page by clicking the link
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        self.assertEqual(self.driver.title, "Register")

    # Registration Page Tests
    def test_registration_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        self.driver.find_element(By.ID, "register_username_field")
        self.driver.find_element(By.ID, "register_password_field")
        self.driver.find_element(By.ID, "confirm_password_field")
        self.driver.find_element(By.ID, "register_button")
        # self.driver.find_element(By.ID, "registration_success_message")
        
    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        # Registering a new user
        username = "newuser"
        password = "newpassword"

        self.driver.find_element(By.ID, "register_username_field").send_keys(username)
        self.driver.find_element(By.ID, "register_password_field").send_keys(password)
        self.driver.find_element(By.ID, "confirm_password_field").send_keys(password)
        self.driver.find_element(By.ID, "register_button").click()

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username}:{password}\n" in users)

    # Dashboard Page Tests
    def test_dashboard_elements(self):
        self.login()
        self.driver.find_element(By.ID, "subscription_list")
        self.driver.find_element(By.ID, "add_subscription_button")
        self.driver.find_element(By.ID, "view_subscription_button")
        self.driver.find_element(By.ID, "contact_us_button")
        self.driver.find_element(By.ID, "logout_button")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_subscription_button").click()
        self.assertIn('Add Subscription', self.driver.title)
        
        self.login()
        self.driver.find_element(By.ID, "view_subscription_button").click()
        self.assertIn("View Subscription", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "contact_us_button").click()
        self.assertIn("Contact Us", self.driver.title)

    # Add Subscription Page Tests
    def test_add_subscription_elements(self):
        self.login()
        self.driver.find_element(By.ID, "add_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_field")
        self.driver.find_element(By.ID, "subscription_frequency_field")
        self.driver.find_element(By.ID, "subscription_start_date_field")
        self.driver.find_element(By.ID, "save_subscription_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_add_subscription_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_field").send_keys("Meat Lovers")
        self.driver.find_element(By.ID, "subscription_frequency_field").send_keys("Daily")
        self.driver.find_element(By.ID, "subscription_start_date_field").send_keys("202409-09-01")
        self.driver.find_element(By.ID, "save_subscription_button").click()

        with open(os.path.join('data', 'subscriptions.txt'), 'r') as file:
            subscriptions = file.readlines()
        self.assertTrue(any("Meat Lovers|Weekly|202409-09-01" in sub for sub in subscriptions))

    # View Subscription Page Tests
    def test_view_subscription_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_display")
        self.driver.find_element(By.ID, "subscription_frequency_display")
        self.driver.find_element(By.ID, "subscription_start_date_display")
        self.driver.find_element(By.ID, "edit_subscription_button")
        self.driver.find_element(By.ID, "delete_subscription_button")
        self.driver.find_element(By.ID, "back_button")

    # Edit Subscription Page Tests
    def test_edit_subscription_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_field").send_keys("Vegan")
        self.driver.find_element(By.ID, "edit_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_field")
        self.driver.find_element(By.ID, "subscription_frequency_field")
        self.driver.find_element(By.ID, "subscription_start_date_field")
        self.driver.find_element(By.ID, "save_subscription_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_edit_subscription_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_field").send_keys("Vegan")
        self.driver.find_element(By.ID, "edit_subscription_button").click()

        self.driver.find_element(By.ID, "subscription_frequency_field").clear()
        self.driver.find_element(By.ID, "subscription_frequency_field").send_keys("Daily")
        self.driver.find_element(By.ID, "save_subscription_button").click()

        with open(os.path.join('data', 'subscriptions.txt'), 'r') as file:
            subscriptions = file.readlines()
        self.assertTrue(any("Vegan|Daily" in sub for sub in subscriptions))
    
    def test_view_subscription_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_field").send_keys("Vegan")
        self.driver.find_element(By.ID, "edit_subscription_button").click()
        self.assertIn("Edit Subscription", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "view_subscription_button").click()
        self.driver.find_element(By.ID, "subscription_type_field").send_keys("Vegan")
        self.driver.find_element(By.ID, "delete_subscription_button").click()

        with open(os.path.join('data', 'subscriptions.txt'), 'r') as file:
            subscriptions = file.readlines()
        self.assertFalse(any("Vegan" in sub for sub in subscriptions))

    # Contact Us Page Tests
    def test_contact_us_elements(self):
        self.login()
        self.driver.find_element(By.ID, "contact_us_button").click()
        self.driver.find_element(By.ID, "contact_name_field")
        self.driver.find_element(By.ID, "contact_email_field")
        self.driver.find_element(By.ID, "contact_message_field")
        self.driver.find_element(By.ID, "send_message_button")
        self.driver.find_element(By.ID, "back_button")

    def test_contact_us_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "contact_us_button").click()
        self.driver.find_element(By.ID, "contact_name_field").send_keys("John Doe")
        self.driver.find_element(By.ID, "contact_email_field").send_keys("john@example.com")
        self.driver.find_element(By.ID, "contact_message_field").send_keys("I need help with my subscription.")
        self.driver.find_element(By.ID, "send_message_button").click()

        with open(os.path.join('data', 'inquiries.txt'), 'r') as file:
            inquiries = file.readlines()
        self.assertTrue(any("John Doe|john@example.com|I need help with my subscription." in inquiry for inquiry in inquiries))

class TestGourmetFoodSubscription:
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
            try:
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
    py = r'path\to\your\GourmetFoodSubscription\app.py'  # Update the path to the actual script location
    test = TestGourmetFoodSubscription(checker, py)
    print(test.main())

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
        self.driver.find_element(By.ID, "error_message")
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
        self.driver.find_element(By.ID, "occupation_field")
        self.driver.find_element(By.ID, "register_button")
        self.driver.find_element(By.ID, "registration_success_message")
        
    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        # Registering a new user
        username = "newuser"
        password = "newpassword"
        occupation = "student"

        self.driver.find_element(By.ID, "register_username_field").send_keys(username)
        self.driver.find_element(By.ID, "register_password_field").send_keys(password)
        self.driver.find_element(By.ID, "confirm_password_field").send_keys(password)
        self.driver.find_element(By.ID, "occupation_field").send_keys(occupation)
        self.driver.find_element(By.ID, "register_button").click()

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username}:{password}:{occupation}\n" in users)

    # Dashboard Page Tests
    def test_dashboard_elements(self):
        self.login()
        self.driver.find_element(By.ID, "posts_list")
        self.driver.find_element(By.ID, "add_post_button")
        self.driver.find_element(By.ID, "search_post_button")
        self.driver.find_element(By.ID, "user_profile_button")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_post_button").click()
        self.assertIn('Add Post', self.driver.title)
        
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.assertIn("Search Post", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "user_profile_button").click()
        self.assertIn("User Profile", self.driver.title)

    # Add Post Page Tests
    def test_add_post_elements(self):
        self.login()
        self.driver.find_element(By.ID, "add_post_button").click()
        self.driver.find_element(By.ID, "post_title_field")
        self.driver.find_element(By.ID, "post_date_field")
        self.driver.find_element(By.ID, "post_category_field")
        self.driver.find_element(By.ID, "post_content_field")
        self.driver.find_element(By.ID, "save_post_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_add_post_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_post_button").click()
        self.driver.find_element(By.ID, "post_title_field").send_keys("My First Post")
        self.driver.find_element(By.ID, "post_date_field").send_keys("202409-08-28")
        self.driver.find_element(By.ID, "post_category_field").send_keys("Banking")
        self.driver.find_element(By.ID, "post_content_field").send_keys("Content about Banking.")
        self.driver.find_element(By.ID, "save_post_button").click()

        with open(os.path.join('data', 'posts.txt'), 'r') as file:
            posts = file.readlines()
        titles = [line.split('|')[2].strip() for line in posts]
        self.assertIn("My First Post", titles)

    # Search Post Page Tests
    def test_search_post_elements(self):
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "investment_button")
        self.driver.find_element(By.ID, "banking_button")
        self.driver.find_element(By.ID, "insurance_button")
        self.driver.find_element(By.ID, "back_button")

    def test_search_post_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "investment_button").click()
        self.assertIn("nvestment", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "banking_button").click()
        self.assertIn("anking", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "insurance_button").click()
        self.assertIn("nsurance", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "back_button").click()
        self.assertIn("Dashboard", self.driver.title)

    # Category Post Page Tests
    def test_category_post_elements(self):
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "investment_button").click()
        self.driver.find_element(By.ID, "post_list")
        self.driver.find_element(By.ID, "post_title_field")
        self.driver.find_element(By.ID, "edit_post_button")
        self.driver.find_element(By.ID, "delete_post_button")
        self.driver.find_element(By.ID, "back_button")

    def test_category_post_functionality(self):
        # Test editing functionality
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "banking_button").click()

        self.driver.find_element(By.ID, "post_title_field").send_keys("Bank Update")
        self.driver.find_element(By.ID, "edit_post_button").click()
        self.assertIn("Bank Update", self.driver.title)

        # Test deletion functionality
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "investment_button").click()

        self.driver.find_element(By.ID, "post_title_field").send_keys("How to Invest")
        self.driver.find_element(By.ID, "delete_post_button").click()

        # Validate that "How to Invest" is no longer in posts.txt
        with open(os.path.join('data', 'posts.txt'), 'r') as file:
            posts = file.readlines()
        titles = [line.split('|')[2].strip() for line in posts]  # Extract the title from each line
        self.assertNotIn("How to Invest", titles)

    # Post Details Page Tests
    def test_post_details_elements(self):
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "banking_button").click()
        self.driver.find_element(By.ID, "post_title_field").send_keys("My First Post")
        self.driver.find_element(By.ID, "edit_post_button").click()

        self.driver.find_element(By.ID, "post_title_field")
        self.driver.find_element(By.ID, "post_date")
        self.driver.find_element(By.ID, "post_category")
        self.driver.find_element(By.ID, "post_content")
        self.driver.find_element(By.ID, "save_button")
        self.driver.find_element(By.ID, "back_button")

    def test_post_details_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "search_post_button").click()
        self.driver.find_element(By.ID, "banking_button").click()
        self.driver.find_element(By.ID, "post_title_field").send_keys("Bank Update")
        self.driver.find_element(By.ID, "edit_post_button").click()

        # Edit the post details
        self.driver.find_element(By.ID, "post_content").clear()
        self.driver.find_element(By.ID, "post_content").send_keys("Updated content about Banking")
        self.driver.find_element(By.ID, "save_button").click()

        with open(os.path.join('data', 'posts.txt'), 'r') as file:
            posts = file.readlines()
        contents = [line.split('|')[4].strip() for line in posts]
        self.assertIn("Updated content about Banking", contents)

    # User Profile Page Tests
    def test_user_profile_elements(self):
        self.login()
        self.driver.find_element(By.ID, "user_profile_button").click()
        self.driver.find_element(By.ID, "profile_username_display")
        self.driver.find_element(By.ID, "profile_occupation_display")
        self.driver.find_element(By.ID, "logout_button")

    def test_user_profile_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "user_profile_button").click()

        self.assertIn("john_doe", self.driver.find_element(By.ID, "profile_username_display").text)
        self.assertIn("banker", self.driver.find_element(By.ID, "profile_occupation_display").text)

        self.driver.find_element(By.ID, "logout_button").click()
        self.assertEqual(self.driver.title, "Login")

class TestPersonalFinanceBlog:
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
            'total': 17,
            'total_basic': 9,
            'total_advanced': 8,
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
    py = r'path\to\your\PersonalFinanceBlog\app.py'  # Update the path to the actual script location
    test = TestPersonalFinanceBlog(checker, py)
    print(test.main())

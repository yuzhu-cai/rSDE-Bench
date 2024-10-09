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

        # Check if redirected to the User Registration Page by checking the title
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
        self.driver.find_element(By.ID, "current_weight_field")
        self.driver.find_element(By.ID, "goal_weight_field")
        self.driver.find_element(By.ID, "register_button")
        # self.driver.find_element(By.ID, "registration_success_message")
        
    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        # Registering a new user
        username = "newuser"
        password = "newpassword"
        current_weight = "80"
        goal_weight = "70"

        self.driver.find_element(By.ID, "register_username_field").send_keys(username)
        self.driver.find_element(By.ID, "register_password_field").send_keys(password)
        self.driver.find_element(By.ID, "confirm_password_field").send_keys(password)
        self.driver.find_element(By.ID, "current_weight_field").send_keys(current_weight)
        self.driver.find_element(By.ID, "goal_weight_field").send_keys(goal_weight)
        self.driver.find_element(By.ID, "register_button").click()

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username}:{password}\n" in users)

        with open(os.path.join('data', 'goals.txt'), 'r') as f:
            goals = f.readlines()
            self.assertTrue(f"{username}|{current_weight}|{goal_weight}\n" in goals)

    # Dashboard Page Tests
    def test_dashboard_elements(self):
        self.login()
        self.assertEqual(self.driver.title, "Dashboard")
        self.driver.find_element(By.ID, "goal_weight")
        self.driver.find_element(By.ID, "current_weight")
        self.driver.find_element(By.ID, "update_goal_button")
        self.driver.find_element(By.ID, "log_activity_button")
        self.driver.find_element(By.ID, "view_activity_button")
        self.driver.find_element(By.ID, "logout_button")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "update_goal_button").click()
        self.assertIn('Update Goal', self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "log_activity_button").click()
        self.assertIn('Log Activity', self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "view_activity_button").click()
        self.assertIn('View Activity', self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "logout_button").click()
        self.assertIn('Login', self.driver.title)

    # Update Goal Page Tests
    def test_update_goal_elements(self):
        self.login()
        self.driver.find_element(By.ID, "update_goal_button").click()
        self.driver.find_element(By.ID, "goal_value_field")
        self.driver.find_element(By.ID, "save_goal_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_update_goal_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "update_goal_button").click()
        new_goal_weight = "75"
        self.driver.find_element(By.ID, "goal_value_field").clear()
        self.driver.find_element(By.ID, "goal_value_field").send_keys(new_goal_weight)
        self.driver.find_element(By.ID, "save_goal_button").click()

        with open(os.path.join('data', 'goals.txt'), 'r') as f:
            goals = f.readlines()
            goal_updated = any(new_goal_weight in line for line in goals)
            self.assertTrue(goal_updated)

    # Log Activity Page Tests
    def test_log_activity_elements(self):
        self.login()
        self.driver.find_element(By.ID, "log_activity_button").click()
        self.driver.find_element(By.ID, "activity_type_field")
        self.driver.find_element(By.ID, "calories_burned_field")
        self.driver.find_element(By.ID, "current_weight_field")
        self.driver.find_element(By.ID, "save_activity_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_log_activity_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "log_activity_button").click()
        activity_type = "Cycling"
        calories_burned = "300"
        current_weight = "90"

        self.driver.find_element(By.ID, "activity_type_field").send_keys(activity_type)
        self.driver.find_element(By.ID, "calories_burned_field").send_keys(calories_burned)
        self.driver.find_element(By.ID, "current_weight_field").send_keys(current_weight)
        self.driver.find_element(By.ID, "save_activity_button").click()

        with open(os.path.join('data', 'activities.txt'), 'r') as f:
            activities = f.readlines()
            activity_logged = any(f"john_doe|{activity_type}|{calories_burned}|{current_weight}" in line for line in activities)
            self.assertTrue(activity_logged)

    # View Activity Page Tests
    def test_view_activity_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_activity_button").click()
        self.driver.find_element(By.ID, "activity_log_list")
        self.driver.find_element(By.ID, "activity_type_field")
        self.driver.find_element(By.ID, "edit_activity_button")
        self.driver.find_element(By.ID, "delete_activity_button")
        self.driver.find_element(By.ID, "back_to_dashboard_button")

    def test_view_activity_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_activity_button").click()
        activity_type = "Running"
        self.driver.find_element(By.ID, "activity_type_field").send_keys(activity_type)
        self.driver.find_element(By.ID, "edit_activity_button").click()
        self.assertIn('Edit Activity', self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "view_activity_button").click()
        activity_type = "Swimming"
        self.driver.find_element(By.ID, "activity_type_field").send_keys(activity_type)
        self.driver.find_element(By.ID, "delete_activity_button").click()

        with open(os.path.join('data', 'activities.txt'), 'r') as f:
            activities = f.readlines()
            activity_deleted = all(activity_type not in line for line in activities)
            self.assertTrue(activity_deleted)

    # Edit Activity Page Tests
    def test_edit_activity_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_activity_button").click()
        self.driver.find_element(By.ID, "activity_type_field").send_keys("Running")
        self.driver.find_element(By.ID, "edit_activity_button").click()
        self.driver.find_element(By.ID, "activity_type_field")
        self.driver.find_element(By.ID, "calories_burned_field")
        self.driver.find_element(By.ID, "current_weight_field")
        self.driver.find_element(By.ID, "save_activity_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_edit_activity_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_activity_button").click()
        self.driver.find_element(By.ID, "activity_type_field").send_keys("Running")
        self.driver.find_element(By.ID, "edit_activity_button").click()

        new_calories_burned = "400"
        self.driver.find_element(By.ID, "calories_burned_field").clear()
        self.driver.find_element(By.ID, "calories_burned_field").send_keys(new_calories_burned)
        self.driver.find_element(By.ID, "save_activity_button").click()

        with open(os.path.join('data', 'activities.txt'), 'r') as f:
            activities = f.readlines()
            activity_updated = any(f"john_doe|Running|400" in line for line in activities)
            activity_deleted = all(f"john_doe|Running|300" not in line for line in activities)
            self.assertTrue(activity_updated)
            self.assertTrue(activity_deleted)

class TestFitnessTracker:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\FitnessTrackerApp\app.py'
    test = TestFitnessTracker(checker, py)
    print(test.main())

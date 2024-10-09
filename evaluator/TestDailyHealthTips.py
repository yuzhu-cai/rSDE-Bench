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
        password = "securepassword"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
    
    # ===== Login Page Tests =====
    def test_login_page_elements(self):
        # Go back to the login page and check elements
        self.assertTrue(self.driver.find_element(By.ID, 'username_field').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'password_field').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'login_button').is_displayed())
    
    def test_login_page_functionality(self):
        # Assume user login is verified by the presence of daily tips page elements
        self.assertIn("User Login", self.driver.title)
        username = "john_doe"
        password = "securepassword"
        self.driver.find_element(By.ID, 'username_field').send_keys(username)
        self.driver.find_element(By.ID, 'password_field').send_keys(password)
        self.driver.find_element(By.ID, 'login_button').click()

        # Check if we are redirected to the daily tips page
        self.assertIn("Daily Health Tips", self.driver.title)

    # ===== Dashboard Page Tests =====
    def test_daily_tips_page_elements(self):
        # Check daily tips page elements after login
        self.login()
        self.assertTrue(self.driver.find_element(By.ID, 'tip_display_area').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'previous_tip_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'next_tip_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'view_tips_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'feedback_form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'feedback_text_area').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'submit_feedback_button').is_displayed())
    
    def test_daily_tips_page_functionality(self):
        # Test functionality of submitting feedback
        self.login()
        self.driver.find_element(By.ID, 'feedback_text_area').send_keys("This is a Test!")
        self.driver.find_element(By.ID, 'submit_feedback_button').click()

        # Verify feedback submission
        with open(os.path.join('data', 'feedback.txt'), 'r') as f:
            feedback_lines = f.readlines()
            self.assertIn("This is a Test!", feedback_lines[-1].strip())
            self.assertIn("john_doe", feedback_lines[-1].strip())
        
        self.login()
        with open(os.path.join('data', 'daily_tips.txt'), 'r') as f:
            daily_tips = f.readlines()
        text_1 = self.driver.find_element(By.ID, 'tip_display_area').text
        self.driver.find_element(By.ID, 'next_tip_button').click()
        text_2 = self.driver.find_element(By.ID, 'tip_display_area').text
        self.driver.find_element(By.ID, 'previous_tip_button').click()
        text_3 = self.driver.find_element(By.ID, 'tip_display_area').text
        self.assertIn(daily_tips[0].split(",")[1].strip(), text_1)
        self.assertIn(daily_tips[1].split(",")[1].strip(), text_2)
        self.assertIn(daily_tips[0].split(",")[1].strip(), text_3)
        self.assertNotEqual(text_1, text_2)
        self.assertEqual(text_1, text_3)

        self.login()
        self.driver.find_element(By.ID, 'view_tips_button').click()
        self.assertIn("Tips Archive", self.driver.title)

    # ===== Tips Archive Page Tests =====
    def test_tips_archive_page_elements(self):
        # Go to the tips archive page
        self.login()
        self.driver.find_element(By.ID, 'view_tips_button').click()
        
        self.assertTrue(self.driver.find_element(By.ID, 'tips_list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'search_tips_form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'search_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'search_button').is_displayed())
    
    def test_tips_archive_page_functionality(self):
        # Test search functionality in the tips archive
        self.login()
        self.driver.find_element(By.ID, 'view_tips_button').click()

        tips_found = self.driver.find_element(By.ID, 'tips_list').text
        with open(os.path.join('data', 'daily_tips.txt'), 'r') as f:
            tips_lines = f.readlines()
        for line in tips_lines:
            self.assertIn(line.split(",")[1].strip(), tips_found)

        self.login()
        self.driver.find_element(By.ID, 'view_tips_button').click()
        self.driver.find_element(By.ID, 'search_input').send_keys("Drink at least 8 glasses of water daily.")
        self.driver.find_element(By.ID, 'search_button').click()

        # Validate if the list contains tips related to "water"
        tips_found = self.driver.find_element(By.ID, 'tips_list').text
        self.assertIn("Drink at least 8 glasses of water daily.", tips_found)
        self.assertNotIn("Incorporate fruits and vegetables into every meal.", tips_found)

class TestDailyHealthTips:
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
    py = r'/Users/caiyuzhu/Dev/asie-bench/codes/ChatDev-updating-4/EcoFriendlyLivingTips/app.py'
    test = TestDailyHealthTips(checker, py)
    import pprint
    pprint.pprint(test.main())
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
        self.driver = webdriver.Chrome()  # Ensure you have the correct driver installed
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.delete_all_cookies()  
        username = 'john_doe'
        password = 'password123'  # Replace with actual password if not hashed

        self.driver.find_element(By.ID,"username").send_keys(username)
        self.driver.find_element(By.ID,"password").send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()

    #Tests for the Login Page
    def test_login_elements(self):
        self.assertTrue(self.driver.find_element(By.ID,"login-form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,"username").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,"password").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,"login-button").is_displayed())

    def test_login_functionality(self):
        
        username = 'john_doe'
        password = 'password123'  # Replace with actual password if not hashed

        self.driver.find_element(By.ID,"username").send_keys(username)
        self.driver.find_element(By.ID,"password").send_keys(password)
        self.driver.find_element(By.ID,"login-button").click()

        # After logging in, expect to navigate to the Festival Listings Page
        
        self.assertIn("Online Cultural Festivals Overview", self.driver.title)
    #Tests for the Festival Listings Page
    def test_festival_overview_elements(self):
        self.login()  # Log in first to access the festivals overview
        self.assertTrue(self.driver.find_element(By.ID,'festivals-list').is_displayed())
        # festival_items = self.driver.find_elements_by_xpath("//*[starts-with(@id, 'festival_item_')]")
        # self.assertGreater(len(festival_items), 0)  # Check at least one festival exists
        self.assertTrue(self.driver.find_element(By.ID,'festival_item_0').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'submit-experience-button').is_enabled())

    def test_festival_overview_functionality(self):
        self.login()  # Ensure elements are present first
        self.driver.find_element(By.ID,'festival_item_0').click()  # Click on the first festival
        time.sleep(1)

        # Verify that we are on the Festival Details page
        self.assertIn("Festival Details", self.driver.title)

    # Tests for the Festival Details Page
    def test_festival_details_elements(self):
        # self.test_festival_overview_functionality() # Navigate to Festival Details first
        self.login()  # Ensure elements are present first
        self.driver.find_element(By.ID,'festival_item_0').click()  # Click on the first festival
        time.sleep(1)        
        self.assertTrue(self.driver.find_element(By.ID,'festival-title').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'festival-info').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'comments-section').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'comment-name').is_displayed())        
        self.assertTrue(self.driver.find_element(By.ID,'comment-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'submit-comment-button').is_enabled())
        self.assertTrue(self.driver.find_element(By.ID,'back-button').is_enabled())

    def test_festival_details_functionality(self):
        # self.test_festival_overview_functionality()  # Ensure elements are present first
        self.login()  # Ensure elements are present first
        self.driver.find_element(By.ID,'festival_item_0').click()  # Click on the first festival
        time.sleep(1)
        # Simulate submitting a comment
        comment_name = 'john_doe'
        comment_text = "Amazing experience!"
        self.driver.find_element(By.ID,'comment-name').send_keys(comment_name)
        self.driver.find_element(By.ID,'comment-input').send_keys(comment_text)
        self.driver.find_element(By.ID,'submit-comment-button').click()
        time.sleep(1)  # Allow comment submission to process

        # Verify if the comment section reflects the new comment - need to read expected from `comments.txt`
        #self.assertIn(comment_text, self.driver.page_source)  # Check if comment is visible
        with open(os.path.join('data', 'comments.txt'), 'r') as file:
            users = file.readlines()
        exists = any("Diwali Festival;john_doe;Amazing experience!" in line for line in users)
        self.assertTrue(exists)

    def test_user_submissions_page_elements(self):
        self.login()  # Ensure we're on festival details for navigation

        self.driver.find_element(By.ID,'submit-experience-button').click()  # Navigate to User Submissions
        time.sleep(1)

        self.assertTrue(self.driver.find_element(By.ID,'submission-form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'user-name').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'experience-description').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID,'submit-button').is_enabled())

    def test_user_submissions_functionality(self):
        self.login()  # Ensure we're on festival details for navigation

        self.driver.find_element(By.ID,'submit-experience-button').click()  # Navigate to User Submissions
        # Simulate submitting an experience
        user_name = "john_doe"
        experience_description = "It was a fantastic festival experience!"

        self.driver.find_element(By.ID,'user-name').send_keys(user_name)
        self.driver.find_element(By.ID,'experience-description').send_keys(experience_description)
        self.driver.find_element(By.ID,'submit-button').click()
        time.sleep(1)  # Allow experience submission to process

        # Verify if the success message appears
        #self.assertTrue(self.driver.find_element(By.ID,'success-message').is_displayed())
        with open(os.path.join('data', 'user_experiences.txt'), 'r') as file:
            users = file.readlines()
        exists = any("john_doe;It was a fantastic festival experience!" in line for line in users)
        self.assertTrue(exists)


class TestOnlineCulturalFestivals:
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
    py = r'C:\Users\84495\Desktop\asie-bench\codes\gpt-4o-mini-2\OnlineCulturalFestivals\app.py'
    test = TestOnlineCulturalFestivals(checker, py)
    print(test.main())






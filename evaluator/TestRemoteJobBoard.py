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
        self.driver.find_element(By.ID, "username-input").send_keys(username)
        self.driver.find_element(By.ID, "password-input").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
    
    # Login Page Tests
    def test_login_elements(self):
        self.driver.get("http://localhost:5000")  # navigate to login page
        self.assertTrue(self.driver.find_element(By.ID, "username-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "login-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "register-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "error-message").is_displayed())

    def test_login_functionality(self):
        self.driver.get("http://localhost:5000")  # navigate to login page
        username = "john_doe"
        password = "password123"
        self.driver.find_element(By.ID, "username-input").send_keys(username)
        self.driver.find_element(By.ID, "password-input").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
        self.assertIn("Home", self.driver.title)
        
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register-button").click()
        self.assertIn("Register", self.driver.title)

    # Register Page Tests
    def test_register_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register-button").click()
        self.assertTrue(self.driver.find_element(By.ID, "username-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "register-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "error-message").is_displayed())

    def test_register_functionality(self):
        self.driver.get("http://localhost:5000")  # navigate to login page
        self.driver.find_element(By.ID, "register-button").click()

        username = "new_user"
        password = "new_password"
        
        self.driver.find_element(By.ID, "username-input").send_keys(username)
        self.driver.find_element(By.ID, "password-input").send_keys(password)
        self.driver.find_element(By.ID, "register-button").click()
        
        with open('data/users.txt', 'r') as f:
            contents = f.read()
            self.assertIn(f"{username},{password}", contents)  # format is username,password,email

    # Home Page Tests
    def test_home_elements(self):
        self.login()
        self.assertTrue(self.driver.find_element(By.ID, "main-content").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-jobs-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "post-job-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "edit-profile-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "login-link").is_displayed())

    def test_home_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        self.assertIn("Job Listings", self.driver.title)
        
        self.login()
        self.driver.find_element(By.ID, "post-job-button").click()
        self.assertIn("Post a Job", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "edit-profile-button").click()
        self.assertIn("User Profile", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "login-link").click()
        self.assertIn("Login", self.driver.title)
        
    # Job Listings Page Tests
    def test_job_listings_elements(self):
        self.login()
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        self.assertTrue(self.driver.find_element(By.ID, "job-list-container").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "job-posting-1").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-button-1").is_displayed())

    def test_job_listings_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "browse-jobs-button").click()
        job_posting = self.driver.find_element(By.ID, "job-posting-1")
        apply_button = job_posting.find_element(By.ID, "apply-button-1")
        apply_button.click()
        
        # Verify application by checking the applied_jobs.txt file
        with open('data/applied_jobs.txt', 'r') as f:
            contents = f.read()
            self.assertIn("john_doe:Software Developer", contents)

    # Post Job Page Tests
    def test_post_job_elements(self):
        self.login()
        self.driver.find_element(By.ID, "post-job-button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "job-title-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "company-name-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "job-description-textarea").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-job-button").is_displayed())
    
    def test_post_job_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "post-job-button").click()
        
        self.driver.find_element(By.ID, "job-title-input").send_keys("QA Engineer")
        self.driver.find_element(By.ID, "company-name-input").send_keys("QA Solutions")
        self.driver.find_element(By.ID, "job-description-textarea").send_keys("Looking for a QA engineer for remote work.")
        self.driver.find_element(By.ID, "submit-job-button").click()

        with open('data/jobs.txt', 'r') as f:
            contents = f.read()
            self.assertIn("QA Engineer,QA Solutions,Looking for a QA engineer for remote work.", contents)

    # Profile Page Tests
    def test_user_profile_elements(self):
        self.login()
        self.driver.find_element(By.ID, "edit-profile-button").click()
        
        self.driver.find_element(By.ID, "username-display").is_displayed()
        self.driver.find_element(By.ID, "email-display").is_displayed()
        self.driver.find_element(By.ID, "edit-profile-button").is_displayed()
        self.driver.find_element(By.ID, "job-list").is_displayed()
        self.driver.find_element(By.ID, "logout-button").is_displayed()

    def test_user_profile_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "edit-profile-button").click()
        self.driver.find_element(By.ID, "logout-button").click()
        self.assertNotIn("Login", self.driver.title)
        
        
        self.login()
        self.driver.find_element(By.ID, "edit-profile-button").click()
        job_list = self.driver.find_element(By.ID, "job-list").text
        with open('data/applied_jobs.txt', 'r') as f:
            jobs = f.readlines()
        joe_job = [job for job in jobs if job.split(":")[0]=="john_doe"]
        n_joe_job = [job for job in jobs if job.split(":")[0]!="john_doe"]
        joe_applied = [job.split(":")[1] for job in joe_job]
        for item in joe_applied:
            self.assertIn(item, job_list)
        for item in n_joe_job:
            self.assertNotIn(item.split(":")[1], job_list)

        previous_name = self.driver.find_element(By.ID, "username-display").get_attribute("value")
        previous_email = self.driver.find_element(By.ID, "email-display").get_attribute("value")
        new_name = "johnDoeUpdated"
        new_email = "abc@bc.com"
        self.driver.find_element(By.ID, "username-display").clear()
        self.driver.find_element(By.ID, "email-display").clear()
        self.driver.find_element(By.ID, "username-display").send_keys(new_name)
        self.driver.find_element(By.ID, "email-display").send_keys(new_email)
        self.driver.find_element(By.ID, "edit-profile-button").click()

        with open('data/users.txt', 'r') as f:
            profiles = f.read()
            self.assertIn(new_name, profiles)
            self.assertIn(new_email, profiles)
            self.assertNotIn(previous_name, profiles)
            self.assertNotIn(previous_email, profiles)
        
        with open('data/applied_jobs.txt', 'r') as f:
            jobs = f.readlines()
        name = [job.split(":")[0] for job in jobs]
        self.assertIn(new_name, name)
        self.assertNotIn(previous_name, name)


class TestRemoteJobBoard:
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
            'total': 13,
            'total_basic': 7,
            'total_advanced': 6,
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\RemoteJobBoard\app.py'
    test = TestRemoteJobBoard(checker, py)
    print(test.main())
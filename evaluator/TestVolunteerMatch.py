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
        username = "username1"
        password = "password1"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
    
    def read_users_data(self):
        with open('data/users.txt', 'r') as f:
            return f.readlines()

    def read_opportunities_data(self):
        with open('data/opportunities.txt', 'r') as f:
            return f.readlines()
    
    # --- Login Page Tests ---

    def test_login_page_elements(self):
        # Check presence of key elements on the Login Page
        self.assertTrue(self.driver.find_element(By.ID, "login-form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "username").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "login-button").is_displayed())

    def test_login_page_functionality(self):
        # Test user login functionality
        self.assertEqual(self.driver.title, "VolunteerMatch - Login")
        username, password = self.read_users_data()[0].strip().split(',')
        
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

        # Validate redirection to the Volunteer Dashboard
        self.assertEqual(self.driver.title, "VolunteerMatch - Dashboard")
    
    # --- Dashboard Page Tests ---

    def test_dashboard_page_elements(self):
        # Navigate to the dashboard page after a successful login
        self.login()
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-header").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "available-opportunities").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "logout-button").is_displayed())

    def test_dashboard_page_functionality(self):
        # Test applying to available opportunities from the dashboard
        self.login()
        opportunities = self.read_opportunities_data()
        
        for opportunity in opportunities:
            opportunity_id, opportunity_title, _ = opportunity.strip().split(',')
            opportunity_element = self.driver.find_element(By.ID, f"opportunity-{opportunity_id}").text
            self.assertIn(opportunity_title, opportunity_element)
            apply_button = self.driver.find_element(By.ID, f"apply-button-{opportunity_id}")
            apply_button.click()
            self.assertEqual(self.driver.title, "VolunteerMatch - Opportunity Details")
            self.driver.back()  # Back to dashboard after testing

            
    # --- Opportunity Details Page Tests ---

    def test_opportunity_details_page_elements(self):
        # Assuming user is logged in and navigated to an opportunity
        self.login()
        print(self.driver.page_source)
        self.driver.find_element(By.ID, "apply-button-1").click()  # Click on the first opportunity
        
        self.assertTrue(self.driver.find_element(By.ID, "opp-details-header").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "opp-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "apply-form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "applicant-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "applicant-email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit-application").is_displayed())

    def test_opportunity_details_page_functionality(self):
        # Test submitting an application from the Opportunity Details Page
        self.login()
        self.driver.find_element(By.ID, "apply-button-1").click()  # Click on the first opportunity
        opp_desc = self.driver.find_element(By.ID, "opp-description").text
        opportunities = self.read_opportunities_data()
        opportunity_id, opportunity_title, opportunity_title_desc = opportunities[0].strip().split(',')
        self.assertIn(opportunity_title_desc, opp_desc)

        applicant_name = "Bob"
        applicant_email = "bob@example.com"
        
        self.driver.find_element(By.ID, "applicant-name").send_keys(applicant_name)
        self.driver.find_element(By.ID, "applicant-email").send_keys(applicant_email)
        self.driver.find_element(By.ID, "submit-application").click()
        
        # Check if the application has been recorded
        with open('data/applications.txt', 'r') as f:
            applications = f.readlines()
        
        self.assertTrue(any(f"{applicant_name},{applicant_email},1\n" in line for line in applications))


class TestVolunteerMatch:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\VolunteerMatch\app.py'
    test = TestVolunteerMatch(checker, py)
    print(test.main())
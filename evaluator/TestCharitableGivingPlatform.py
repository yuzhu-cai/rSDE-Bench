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
        username = "johnDoe"
        password = "password123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "usernameInput").send_keys(username)
        self.driver.find_element(By.ID, "passwordInput").send_keys(password)
        self.driver.find_element(By.ID, "loginButton").click()
    
    # ===== Login Page Tests =====
    def test_login_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "loginPage").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "usernameInput").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "passwordInput").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "loginButton").is_displayed())

    def test_login_page_functionality(self):
        # Assuming a valid user exists in 'users.txt'
        self.assertIn("Login", self.driver.title)
        username = "johnDoe"
        password = "password123"

        self.driver.find_element(By.ID, "usernameInput").send_keys(username)
        self.driver.find_element(By.ID, "passwordInput").send_keys(password)
        self.driver.find_element(By.ID, "loginButton").click()
        self.assertIn("Dashboard", self.driver.title)

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.login()

        # Check presence of essential elements on the Dashboard page
        self.assertTrue(self.driver.find_element(By.ID, "dashboardPage").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "charityList").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "charityDetailsButton").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "myContributions").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "logoutButton").is_displayed())

    def test_dashboard_page_functionality(self):
        self.login()
        
        with open('data/contributions.txt', 'r') as file:
            contributions = file.readlines()
        self.assertIn("johnDoe,SaveTheWhales,20\n", contributions)

        charity_name = [line.split(",")[1].strip() for line in contributions if line.split(",")[0].strip() == "johnDoe"]
        amount = [line.split(",")[2].strip() for line in contributions if line.split(",")[0].strip() == "johnDoe"]
        myContributions = self.driver.find_element(By.ID, "myContributions").text
        for item in charity_name:
            self.assertIn(item, myContributions)
        for item in amount:
            self.assertIn(item, myContributions)

        self.login()
        charityList = self.driver.find_element(By.ID, "charityList").text
        with open('data/charities.txt', 'r') as file:
            charities = file.readlines()
        charity_name = [line.split(",")[0].strip() for line in charities]
        for item in charity_name:
            self.assertIn(item ,charityList)
        
        self.driver.find_element(By.ID, "charityDetailsButton").click()
        self.assertIn("Charity Details", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "logoutButton").click()
        self.assertIn("Login", self.driver.title)


    # ===== Charity Details Page Tests =====
    def test_charity_details_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "charityDetailsButton").click() 
        
        # Check presence of essential elements on the Charity Details page
        self.assertTrue(self.driver.find_element(By.ID, "charityDetailsPage").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "charityTitle").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "charityDescription").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "donationInput").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "donateButton").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "backToDashboardButton").is_displayed())

    def test_charity_details_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "charityDetailsButton").click() 

        with open('data/charities.txt', 'r') as file:
            charities = file.readlines()
        charity_name = [line.split(",")[0].strip() for line in charities][0]
        mission_description = [line.split(",")[1].strip() for line in charities][0]
        self.assertIn(charity_name, self.driver.find_element(By.ID, "charityTitle").text)
        self.assertIn(mission_description, self.driver.find_element(By.ID, "charityDescription").text)

        # Check if the contribution was recorded
        self.driver.find_element(By.ID, "donationInput").send_keys("500")
        self.driver.find_element(By.ID, "donateButton").click()

        with open('data/contributions.txt', 'r') as file:
            contributions = file.readlines()

        self.assertIn(f"johnDoe,{charity_name},500", contributions)  # Replace SomeCharity with actual charity name

        self.login()
        self.driver.find_element(By.ID, "backToDashboardButton").click()
        self.assertIn("Dashboard", self.driver.title)


class TestCharitableGivingPlatform:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\CharitableGivingPlatform\app.py'
    test = TestCharitableGivingPlatform(checker, py)
    print(test.main())
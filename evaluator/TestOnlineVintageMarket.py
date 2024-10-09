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
        username = "johndoe"
        password = "password123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
    
    # ===== Login Page Tests =====
    def test_login_page_elements(self):
        print(self.driver.page_source)
        self.driver.find_element(By.ID, 'login-form')
        self.driver.find_element(By.ID, 'username')
        self.driver.find_element(By.ID, 'password')
        self.driver.find_element(By.ID, 'login-button')

    def test_login_page_functionality(self):
        # Assuming valid login credentials are in users.txt (for example johndoe/password123)
        self.assertIn("Login", self.driver.title)
        self.driver.find_element(By.ID, 'username').send_keys('johndoe')
        self.driver.find_element(By.ID, 'password').send_keys('password123')
        self.driver.find_element(By.ID, 'login-button').click()
        
        self.assertIn("Home", self.driver.title)

    # ===== Home Page Tests =====
    def test_home_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'header')
        self.driver.find_element(By.ID, 'item-list')
        self.driver.find_element(By.ID, 'create-listing-button')
        self.driver.find_element(By.ID, 'search-field')
        self.driver.find_element(By.ID, 'search-button')
        self.driver.find_element(By.ID, 'search-result')
        self.driver.find_element(By.ID, 'item-details-button')

    def test_home_page_functionality(self):
        # Perform a search on the homepage
        self.login()
        self.driver.find_element(By.ID, 'search-field').send_keys('Vintage Clock')
        self.driver.find_element(By.ID, 'search-button').click()
        search_result = self.driver.find_element(By.ID, 'search-result').text
        self.assertIn("Vintage Clock", search_result)

        self.login()
        self.driver.find_element(By.ID, 'create-listing-button').click()
        self.assertIn("Create Listing", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'item-details-button').click()
        self.assertIn("Item Details", self.driver.title)

        self.login()
        item_list = self.driver.find_element(By.ID, 'item-list').text
        with open(os.path.join("data", "listings.txt"), "r") as file:
            listing = file.readlines()
        item_names = [line.split(",")[0].strip() for line in listing]
        for name in item_names:
            self.assertIn(name, item_list)

    # ===== Listing Page Tests =====
    def test_listing_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'create-listing-button').click()
        
        self.driver.find_element(By.ID, 'listing-form')
        self.driver.find_element(By.ID, 'item-name')
        self.driver.find_element(By.ID, 'item-description')
        self.driver.find_element(By.ID, 'item-price')
        self.driver.find_element(By.ID, 'submit-listing-button')

    def test_listing_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'create-listing-button').click()

        self.driver.find_element(By.ID, 'item-name').send_keys('Test Item')
        self.driver.find_element(By.ID, 'item-description').send_keys('This is a test description')
        self.driver.find_element(By.ID, 'item-price').send_keys('10.00')
        self.driver.find_element(By.ID, 'submit-listing-button').click()
        
        with open(os.path.join("data", "listings.txt"), "r") as f:
            data = f.readlines()
        self.assertIn("Test Item,This is a test description,10.00\n", data)
    
    # ===== Item Details Page Tests =====
    def test_item_details_page_elements(self):
        self.login()
        self.driver.find_elements(By.ID, 'item-details-button')[0].click()
        
        self.driver.find_element(By.ID, 'item-title')
        self.driver.find_element(By.ID, 'item-description')
        self.driver.find_element(By.ID, 'item-price')
        self.driver.find_element(By.ID, 'back-button')

    def test_item_details_page_functionality(self):
        self.login()
        self.driver.find_elements(By.ID, 'item-details-button')[0].click()

        item_title = self.driver.find_element(By.ID, 'item-title').text
        item_description = self.driver.find_element(By.ID, 'item-description').text
        item_price = self.driver.find_element(By.ID, 'item-price').text
        with open(os.path.join("data", "listings.txt"), "r") as f:
            data = f.readlines()
        title = data[0].split(",")[0].strip()
        desc = data[0].split(",")[1].strip()
        price = data[0].split(",")[2].strip()
        self.assertIn(title, item_title)
        self.assertIn(desc, item_description)
        self.assertIn(price, item_price)


class TestOnlineVintageMarket:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\OnlineVintageMarket\app.py'
    test = TestOnlineVintageMarket(checker, py)
    print(test.main())
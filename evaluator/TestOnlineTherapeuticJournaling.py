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
        password = "password1"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username-input").send_keys(username)
        self.driver.find_element(By.ID, "password-input").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
    
    # Login Page Tests
    def test_login_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "login-form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "username-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "login-button").is_displayed())

    def test_login_page_functionality(self):
        self.assertIn("User Login", self.driver.title)
        self.driver.find_element(By.ID, "username-input").send_keys("john_doe")
        self.driver.find_element(By.ID, "password-input").send_keys("password1") # Use the actual hashed password for your test
        self.driver.find_element(By.ID, "login-button").click()
        
        self.assertIn("User Dashboard", self.driver.title)

    # Dashboard Page Tests
    def test_dashboard_page_elements(self):
        self.login()
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-header").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "create-entry-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "entry-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "edit-entry-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "about-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "logout-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "create-entry-button").click()
        self.assertIn("New Journal Entry", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "edit-entry-button").click()
        self.assertIn("Edit Journal Entry", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "about-button").click()
        self.assertIn("About Us", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "logout-button").click()
        self.assertIn("User Login", self.driver.title)

        self.login()
        entry_list = self.driver.find_element(By.ID, "entry-list").text
        with open(os.path.join("data", "entries.txt"), 'r') as file:
            entries = file.readlines()
        titles = [line.split("|")[2].strip() for line in entries]
        contents = [line.split("|")[3].strip() for line in entries]
        self.assertIn(titles[0], entry_list)
        self.assertIn(contents[0], entry_list)

    # Create Journal Entry Page Tests
    def test_create_journal_entry_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "create-entry-button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "entry-form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "entry-title-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "entry-content-textarea").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "save-entry-button").is_displayed())

    def test_create_journal_entry_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "create-entry-button").click()
        self.driver.find_element(By.ID, "entry-title-input").send_keys("My Test Entry")
        self.driver.find_element(By.ID, "entry-content-textarea").send_keys("This is a test entry content.")
        self.driver.find_element(By.ID, "save-entry-button").click()
        
        with open(os.path.join("data", "entries.txt"), 'r') as file:
            entries = file.readlines()
        self.assertIn("3|john_doe|My Test Entry|This is a test entry content.|", entries[-1].strip())

    # Edit Journal Entry Page Tests
    def test_edit_journal_entry_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "edit-entry-button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "edit-entry-form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "edit-title-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "edit-content-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "update-entry-button").is_displayed())

    def test_edit_journal_entry_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "edit-entry-button").click()
        self.test_edit_journal_entry_page_elements()  # Verify elements first
        entry_title_input = self.driver.find_element(By.ID, "edit-title-input")
        entry_content_input = self.driver.find_element(By.ID, "edit-content-input")

        previous_title = entry_title_input.get_attribute("value")
        previous_content = entry_content_input.get_attribute("value")

        self.assertIn("My First Entry", previous_title)
        self.assertIn("Today I felt happy.", previous_content)
        
        # Modifying the existing entry
        entry_title_input.clear()
        entry_title_input.send_keys("Updated Test Entry Title")
        entry_content_input.clear()
        entry_content_input.send_keys("Updated Test Entry Content.")
        self.driver.find_element(By.ID, "update-entry-button").click()

        with open(os.path.join("data", "entries.txt"), 'r') as file:
            entries = file.readlines()
        self.assertIn("1|john_doe|Updated Test Entry Title|Updated Test Entry Content.|", entries[0].strip())
        self.assertNotIn("1|john_doe|My First Entry|Today I felt happy.|", entries[0].strip())
        

    # About Page Tests
    def test_about_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "about-button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "about-header").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "about-description").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "contact-info").is_displayed())

    def test_about_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "about-button").click()
        self.assertIsNotNone(self.driver.find_element(By.ID, "about-header").text)
        self.assertIsNotNone(self.driver.find_element(By.ID, "about-description").text)
        self.assertIsNotNone(self.driver.find_element(By.ID, "contact-info").text)

class TestOnlineTherapeuticJournaling:
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
            'total': 11,
            'total_basic': 6,
            'total_advanced': 5,
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\OnlineTherapeuticJournaling\app.py'
    test = TestOnlineTherapeuticJournaling(checker, py)
    print(test.main())
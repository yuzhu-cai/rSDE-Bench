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
    
    # ===== Login Page Tests =====
    def test_login_page_elements(self):
        # Check the presence of elements on the Login page
        self.driver.find_element(By.ID, "login-page")
        self.driver.find_element(By.ID, "username-input")
        self.driver.find_element(By.ID, "password-input")
        self.driver.find_element(By.ID, "login-button")

    def test_login_page_functionality(self):
        self.assertIn("Login", self.driver.title)
        # Perform a login operation and verify username in profiles.txt
        self.driver.find_element(By.ID, "username-input").send_keys("john_doe")
        self.driver.find_element(By.ID, "password-input").send_keys("password123")
        self.driver.find_element(By.ID, "login-button").click()
        
        self.assertIn("Community Feed", self.driver.title)
        

    # ===== Community Feed Page Tests =====
    def test_community_feed_elements(self):
        # Navigate to Community Feed page
        self.login()

        # Check elements
        self.driver.find_element(By.ID, "feed-page")
        self.driver.find_element(By.ID, "post-input")
        self.driver.find_element(By.ID, "post-button")
        self.driver.find_element(By.ID, "feed-container")
        self.driver.find_element(By.ID, "resource-button")
        self.driver.find_element(By.ID, "profile-button")
        self.driver.find_element(By.ID, "post-1")

    def test_community_feed_functionality(self):
        self.login()

        # Navigate to post something on the feed
        self.driver.find_element(By.ID, "post-input").send_keys("This is a test post!")
        self.driver.find_element(By.ID, "post-button").click()

        # Check if the post appears in feed-container
        post_content = self.driver.find_element(By.ID, "post-3").text  # Assuming first post
        self.assertIn("This is a test post!", post_content)
        with open(os.path.join('data', 'posts.txt'), 'r') as f:
            posts = f.readlines()
        self.assertIn('3', posts[-1])
        self.assertIn('john_doe', posts[-1])
        self.assertIn('This is a test post!', posts[-1])

        self.login()
        self.driver.find_element(By.ID, "resource-button").click()
        self.assertIn("Resources", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "profile-button").click()
        self.assertIn("User Profile", self.driver.title)

    # ===== Resources Page Tests =====
    def test_resources_page_elements(self):
        # Navigate to Resources page
        self.login()
        self.driver.find_element(By.ID, "resource-button").click()

        # Check elements
        self.driver.find_element(By.ID, "resources-page")
        self.driver.find_element(By.ID, "resource-container")
        resource_titles = self.driver.find_elements(By.ID, "resource-title")
        resource_descriptions = self.driver.find_elements(By.ID, "resource-description")
        links = self.driver.find_elements(By.ID, "link")
        self.assertTrue(len(resource_titles) > 0)
        self.assertTrue(len(resource_descriptions) > 0)
        self.assertTrue(len(links) > 0)

    def test_resources_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "resource-button").click()

        # Verify resources match the data in resources.txt
        with open('data/resources.txt', 'r') as resource_file:
            resources = resource_file.readlines()
        resource_titles = self.driver.find_elements(By.ID, "resource-title")
        resource_descriptions = self.driver.find_elements(By.ID, "resource-description")
        links = self.driver.find_elements(By.ID, "link")
        self.assertEqual(len(resource_titles), len(resource_descriptions))
        self.assertEqual(len(resource_titles), len(links))
    
        for i in range(len(links)):
            self.assertIn(f"{resource_titles[i].text},{resource_descriptions[i].text},{links[i].get_attribute('href')}\n", resources)
    
    # ===== User Profile Page Tests =====
    def test_profile_page_elements(self):
        # Navigate to Profile page
        self.login()
        self.driver.find_element(By.ID, "profile-button").click()

        # Check elements on profile page
        self.driver.find_element(By.ID, "profile-page")
        self.driver.find_element(By.ID, "username-display")
        self.driver.find_element(By.ID, "pet-details")
        self.driver.find_element(By.ID, "pet-name")
        self.driver.find_element(By.ID, "pet-age")
        self.driver.find_element(By.ID, "pet-name-input")
        self.driver.find_element(By.ID, "pet-age-input")
        self.driver.find_element(By.ID, "save-button")
        self.driver.find_element(By.ID, "logout-button")

    def test_profile_page_functionality(self):
        # Update pet details and verify updated values against profiles.txt
        self.login()
        self.driver.find_element(By.ID, "profile-button").click()

        self.assertIn("john_doe", self.driver.find_element(By.ID, "username-display").text)
        self.assertIn("Max", self.driver.find_element(By.ID, "pet-name").text)
        self.assertIn("3", self.driver.find_element(By.ID, "pet-age").text)
        self.assertNotIn("Luna", self.driver.find_element(By.ID, "pet-name").text)
        self.assertNotIn("1", self.driver.find_element(By.ID, "pet-age").text)

        self.driver.find_element(By.ID, "pet-name-input").clear()
        self.driver.find_element(By.ID, "pet-name-input").send_keys("Buddy")
        self.driver.find_element(By.ID, "pet-age-input").clear()
        self.driver.find_element(By.ID, "pet-age-input").send_keys("5")
        self.driver.find_element(By.ID, "save-button").click()

        # Check updated profile
        with open('data/profiles.txt', 'r') as profile_file:
            profiles = profile_file.readlines()
        self.assertIn("john_doe,Buddy,5\n", profiles)

        self.login()
        self.driver.find_element(By.ID, "logout-button").click()
        self.assertIn("Login", self.driver.title)

class TestPetCareCommunity:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\PetCareCommunity\app.py'
    test = TestPetCareCommunity(checker, py)
    print(test.main())
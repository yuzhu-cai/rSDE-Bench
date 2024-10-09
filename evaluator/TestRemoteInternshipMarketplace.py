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
        self.driver.find_element(By.ID, "input_username").send_keys(username)
        self.driver.find_element(By.ID, "input_password").send_keys(password)
        self.driver.find_element(By.ID, "btn_login").click()
    
    # Login Page Tests
    def test_login_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, 'input_username').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_password').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_login').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'link_register').is_displayed())

    def test_login_page_functionality(self):
        self.assertIn("User Login", self.driver.title)
        # Test the login process
        username = 'john_doe'  # Example username
        password = 'securepassword'  # Example password

        self.driver.find_element(By.ID, 'input_username').send_keys(username)
        self.driver.find_element(By.ID, 'input_password').send_keys(password)
        self.driver.find_element(By.ID, 'btn_login').click()
        self.assertIn("Internships Dashboard", self.driver.title)

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'link_register').click()
        self.assertIn("User Registration", self.driver.title)
    
    # Registration Page Tests
    def test_registration_page_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'link_register').click()

        self.assertTrue(self.driver.find_element(By.ID, 'input_username').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_first_name').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_last_name').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_email').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_password').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_confirm_password').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_register').is_displayed())

    def test_registration_page_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'link_register').click()

        username = 'new_user'
        first_name = 'First'
        last_name = 'Last'
        email = 'new_user@example.com'
        password = 'newpassword'

        self.driver.find_element(By.ID, 'input_username').send_keys(username)
        self.driver.find_element(By.ID, 'input_first_name').send_keys(first_name)
        self.driver.find_element(By.ID, 'input_last_name').send_keys(last_name)
        self.driver.find_element(By.ID, 'input_email').send_keys(email)
        self.driver.find_element(By.ID, 'input_password').send_keys(password)
        self.driver.find_element(By.ID, 'input_confirm_password').send_keys(password)
        self.driver.find_element(By.ID, 'btn_register').click()

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
        self.assertIn(f"{username},{password},{first_name},{last_name},{email}\n", users)
    
    # Dashboard Page Tests
    def test_dashboard_page_elements(self):
        self.login()

        self.assertTrue(self.driver.find_element(By.ID, 'heading_welcome').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_view_internships').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_post_internship').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'list_internships').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_logout').is_displayed())

    def test_dashboard_page_functionality(self):
        # User login and dashboard interaction
        self.login()
        self.assertIn("welcome", self.driver.find_element(By.ID, 'heading_welcome').text.lower())

        list_internships = self.driver.find_element(By.ID, 'list_internships').text
        with open(os.path.join('data', 'internships.txt'), 'r') as f:
            internships = f.readlines()
        titles = [line.split(",")[1].strip() for line in internships]
        for title in titles:
            self.assertIn(title, list_internships)

        self.driver.find_element(By.ID, 'btn_view_internships').click()
        self.assertIn("Available Internships", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'btn_post_internship').click()
        self.assertIn("Post a New Internship", self.driver.title)

    # Internship Listings Page Tests
    def test_internship_listings_page_elements(self):
        # Navigate to Dashboard first
        self.login()
        self.driver.find_element(By.ID, 'btn_view_internships').click()

        self.assertTrue(self.driver.find_element(By.ID, 'input_search').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_search_intership').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'list_results').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'list_available_internships').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_view_details_1').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_view_details_2').is_displayed())

    def test_internship_listings_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'btn_view_internships').click()

        # Perform a search for an internship
        self.driver.find_element(By.ID, 'input_search').send_keys('Software Development Internship')
        self.driver.find_element(By.ID, 'btn_search_intership').click()
        result = self.driver.find_element(By.ID, 'list_results').text
        with open(os.path.join('data', 'internships.txt'), 'r') as f:
            internships = f.readlines()
        items = internships[0].split(",")
        for item in items:
            self.assertIn(item.strip(), result)

        self.login()
        list_available_internships = self.driver.find_element(By.ID, 'list_available_internships').text
        internship_ids = [line.split(",")[0].strip() for line in internships]
        titles = [line.split(",")[1].strip() for line in internships]
        for item in internship_ids:
            self.assertIn(item, list_available_internships)
        for item in titles:
            self.assertIn(item, list_available_internships)
        
        self.driver.find_element(By.ID, 'btn_view_details_1').click()
        self.assertIn("Internship Details", self.driver.title)

    # Post Internship Page Tests
    def test_post_internship_page_elements(self):
        # Navigate to Post Internship Page
        self.login()
        self.driver.find_element(By.ID, 'btn_post_internship').click()

        self.assertTrue(self.driver.find_element(By.ID, 'input_internship_title').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_internship_desc').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_internship_category').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'input_application_deadline').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_submit_internship').is_displayed())

    def test_post_internship_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'btn_post_internship').click()

        # Post an internship
        self.driver.find_element(By.ID, 'input_internship_title').send_keys('New Software Internship')
        self.driver.find_element(By.ID, 'input_internship_desc').send_keys('A remote internship in software development.')
        self.driver.find_element(By.ID, 'input_internship_category').send_keys('Software')
        self.driver.find_element(By.ID, 'input_application_deadline').send_keys('202309-12-31')
        self.driver.find_element(By.ID, 'btn_submit_internship').click()

        with open(os.path.join('data', 'internships.txt'), 'r') as f:
            internships = f.readlines()
        self.assertIn("3,New Software Internship,A remote internship in software development.,Software,202309-12-31\n", internships)
    
    # Internship Details Page Tests
    def test_internship_details_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'btn_view_internships').click()
        self.driver.find_element(By.ID, 'btn_view_details_2').click()

        self.assertTrue(self.driver.find_element(By.ID, 'heading_internship_title').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'para_internship_desc').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'para_internship_cate').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'para_internship_ddl').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_apply_now').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'btn_back_to_listings').is_displayed())

    def test_internship_details_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'btn_view_internships').click()
        self.driver.find_element(By.ID, 'btn_view_details_2').click()

        # Apply for the internship
        self.assertIn("Test", self.driver.find_element(By.ID, 'heading_internship_title').text)
        self.assertIn("ABC", self.driver.find_element(By.ID, 'para_internship_desc').text)
        self.assertIn("CDR", self.driver.find_element(By.ID, 'para_internship_cate').text)
        self.assertIn("2024-12-31", self.driver.find_element(By.ID, 'para_internship_ddl').text)

        self.driver.find_element(By.ID, 'btn_apply_now').click()
        with open(os.path.join('data', 'applications.txt'), 'r') as f:
            applications = f.readlines()
        self.assertIn("2,john_doe,2", applications[1])

class TestRemoteInternshipMarketplace:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\RemoteInternshipMarketplace\app.py'
    test = TestRemoteInternshipMarketplace(checker, py)
    print(test.main())
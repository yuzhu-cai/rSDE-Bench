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
        # Initialize the web driver (Assuming Chrome)
        self.driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
        self.driver.get("http://localhost:5000")
    
    def tearDown(self):
        self.driver.quit()

    def login(self):
        driver = self.driver
        users = self.read_users_data()
        # Attempting successful login with the first user
        username, password = users[0]
        driver.find_element(By.ID,'username').send_keys(username)
        driver.find_element(By.ID,'password').send_keys(password)
        driver.find_element(By.ID,'login-button').click()
        
        # Verify redirection to Home Page

    def read_users_data(self):
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            return [line.strip().split(',') for line in f.readlines()]

    def read_exchanges_data(self):
        with open(os.path.join('data', 'exchanges.txt'), 'r') as f:
            return [line.strip().split(',') for line in f.readlines()]

    def test_login_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID,'login-form').is_displayed())  # Check presence of login form
        self.assertTrue(driver.find_element(By.ID,'username').is_displayed())     # Check presence of username field
        self.assertTrue(driver.find_element(By.ID,'password').is_displayed())     # Check presence of password field
        self.assertTrue(driver.find_element(By.ID,'login-button').is_displayed()) # Check presence of login button
        # self.assertTrue(driver.find_element(By.ID,'error-message').is_displayed()) # Check presence of error message container
    
    def test_login_functionality(self):
        driver = self.driver
        users = self.read_users_data()
        # Attempting successful login with the first user
        username, password = users[0]
        driver.find_element(By.ID,'username').send_keys(username)
        driver.find_element(By.ID,'password').send_keys(password)
        driver.find_element(By.ID,'login-button').click()
        
        # Verify redirection to Home Page
        self.assertIn("Home", driver.title)

    def test_home_elements(self):
        driver = self.driver
        # After login we need to navigate to Home Page
        self.login()
        
        #self.assertTrue(driver.find_element(By.ID,'welcome-message').is_displayed())   # Check presence of welcome message
        self.assertTrue(driver.find_element(By.ID,'culture-list').is_displayed())      # Check presence of culture list
        self.assertTrue(driver.find_element(By.ID,'profile-link').is_displayed())      # Check presence of profile link
        self.assertTrue(driver.find_element(By.ID,'contact-link').is_displayed())      # Check presence of contact link

    def test_home_functionality(self):
        driver = self.driver
        # Assuming the user is on the Home Page after login
        self.login()
        
        # Ensure that search functionality works (search for a term that is assumed to be present)
        driver.find_element(By.ID,'profile-link').click()
        
        self.assertIn("Profile", driver.title) 

        driver.find_element(By.ID,'home-link').click()
        
        # Ensure that search functionality works (search for a term that is assumed to be present)
        driver.find_element(By.ID,'contact-link').click()
        
        self.assertIn("Contact", driver.title) 
        driver.find_element(By.ID,'home-link').click()
        
        # Ensure that search functionality works (search for a term that is assumed to be present)
        driver.find_element(By.ID,'culture-item-0').click()
        
        self.assertIn("Cultural Exchange", driver.title) 

    def test_exchange_elements(self):
        driver = self.driver
        # Navigate to Home Page and then to Cultural Exchange Page
        self.login()
        driver.find_element(By.ID,'culture-item-0').click()        
        self.assertTrue(driver.find_element(By.ID,'exchange-form').is_displayed())        # Check presence of exchange form
        self.assertTrue(driver.find_element(By.ID,'title').is_displayed())                # Check presence of title input
        self.assertTrue(driver.find_element(By.ID,'description').is_displayed())          # Check presence of description textarea
        self.assertTrue(driver.find_element(By.ID,'submit-exchange').is_displayed())      # Check presence of submit button
        self.assertTrue(driver.find_element(By.ID,'exchange-list').is_displayed())        # Check presence of exchange list

    def test_exchange_functionality(self):
        driver = self.driver
        # Navigate to Cultural Exchange
        self.test_exchange_elements()
        
        # Submit a new exchange
        title = "Cultural Title Test"
        description = "Description of cultural exchange test"
        driver.find_element(By.ID,'title').send_keys(title)
        driver.find_element(By.ID,'description').send_keys(description)
        driver.find_element(By.ID,'submit-exchange').click()
        with open(os.path.join('data', 'exchanges.txt'), 'r') as file:
            users = file.readlines()
        exists = any("Cultural Title Test,Description of cultural exchange test" in line for line in users)
        self.assertTrue(exists)
    def test_profile_elements(self):
        driver = self.driver
        # Login to go to the Home Page then to Profile Page
        self.login()
        
        # Ensure that search functionality works (search for a term that is assumed to be present)
        driver.find_element(By.ID,'profile-link').click()
        
        self.assertTrue(driver.find_element(By.ID,'profile-header').is_displayed())       # Check presence of profile header
        self.assertTrue(driver.find_element(By.ID,'username-display').is_displayed())      # Check presence of username display
        self.assertTrue(driver.find_element(By.ID,'logout-button').is_displayed())         # Check presence of logout button
        self.assertTrue(driver.find_element(By.ID,'home-link').is_displayed())         # Check presence of logout button

    def test_profile_functionality(self):
        driver = self.driver
        # Go to the profile page
        self.login()
        
        # Ensure that search functionality works (search for a term that is assumed to be present)
        driver.find_element(By.ID,'profile-link').click()
        
        #username = self.read_users_data()[0][0]  # Get username from data

        driver.find_element(By.ID,'logout-button').click()
        self.assertIn("Login", driver.title)
        # Validate that changes were made (assuming bio is displayed again)

    def test_contact_elements(self):
        driver = self.driver
        # Login to go to Home Page and then to Contact Page
        self.login()
        
        # Ensure that search functionality works (search for a term that is assumed to be present)

        driver.find_element(By.ID,'contact-link').click()    # Click on contact link
        
        self.assertTrue(driver.find_element(By.ID,'contact-form').is_displayed())            # Check presence of contact form
        self.assertTrue(driver.find_element(By.ID,'contact-name').is_displayed())            # Check presence of contact name field
        self.assertTrue(driver.find_element(By.ID,'contact-email').is_displayed())           # Check presence of contact email field
        self.assertTrue(driver.find_element(By.ID,'contact-message').is_displayed())         # Check presence of contact message textarea
        self.assertTrue(driver.find_element(By.ID,'send-message-button').is_displayed())     # Check presence of send message button

    def test_contact_functionality(self):
        driver = self.driver
        # Go to Contact Page
        self.login()
        
        # Ensure that search functionality works (search for a term that is assumed to be present)

        driver.find_element(By.ID,'contact-link').click()    # Click on contact link
        
        name = "Test Name"
        email = "test@example.com"
        message = "This is a test message."
        driver.find_element(By.ID,'contact-name').send_keys(name)
        driver.find_element(By.ID,'contact-email').send_keys(email)
        driver.find_element(By.ID,'contact-message').send_keys(message)
        driver.find_element(By.ID,'send-message-button').click()
        
        # Verify user registration by checking user data file
        with open(os.path.join('data', 'contacts.txt'), 'r') as file:
            users = file.readlines()
        exists = any("Test Name,test@example.com,This is a test message." in line for line in users)
        self.assertTrue(exists)

class TestOnlineCulturalExchange:
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
    py = r'C:\Users\84495\Desktop\asie-bench\codes\gemini-1.5-flash-0\OnlineCulturalExchange\app.py'
    test = TestOnlineCulturalExchange(checker, py)
    print(test.main())

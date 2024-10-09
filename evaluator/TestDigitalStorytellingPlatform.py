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
        """Set up the testing environment, including initializing the WebDriver."""
        self.driver = webdriver.Chrome()  # Ensure that you have Chromedriver installed and in PATH
        self.driver.get("http://localhost:5000")  # Navigates to the landing page

    def tearDown(self):
        """Close the browser window after each test."""
        self.driver.quit()

    # Login Page Tests
    def test_login_page_elements(self):
        """Test the presence and accessibility of critical elements on the Login Page."""
        self.driver.get("http://localhost:5000/login")  # Go to the login page
        time.sleep(1)  # Wait for the page to load

        assert self.driver.find_element(By.ID, "username_field")
        assert self.driver.find_element(By.ID, "password_field")
        assert self.driver.find_element(By.ID, "login_button")
        assert self.driver.find_element(By.ID, "register_link")

    def test_login_page_functionality(self):
        """Test the login functionality."""
        self.driver.get("http://localhost:5000/login")
        time.sleep(1)

        # Fill out the login form
        self.driver.find_element(By.ID, "username_field").send_keys("johndoe")
        self.driver.find_element(By.ID, "password_field").send_keys("password123")
        self.driver.find_element(By.ID, "login_button").click()

        time.sleep(1)  # Wait for redirection
        self.assertIn("Create Your Story", self.driver.title)  # Validate redirection to Story Creation Page

    # Registration Page Tests
    def test_registration_page_elements(self):
        """Test the presence and accessibility of critical elements on the Registration Page."""
        self.driver.get("http://localhost:5000/register")  # Go to the registration page
        time.sleep(1)

        assert self.driver.find_element(By.ID, "reg_username_input")
        assert self.driver.find_element(By.ID, "reg_password_input")
        assert self.driver.find_element(By.ID, "reg_email_input")
        assert self.driver.find_element(By.ID, "register_button")

    def test_registration_page_functionality(self):
        """Test user registration functionality."""
        self.driver.get("http://localhost:5000/register")
        time.sleep(1)

        # Register a new user
        self.driver.find_element(By.ID, "reg_username_input").send_keys("newuser")
        self.driver.find_element(By.ID, "reg_password_input").send_keys("newpassword")
        self.driver.find_element(By.ID, "reg_email_input").send_keys("newuser@example.com")
        self.driver.find_element(By.ID, "register_button").click()

        time.sleep(1)  # Wait for redirection
        self.assertIn("User Login", self.driver.title)  # Validate redirection to Login Page
        
        # Validate that the new user details are stored correctly
        with open(os.path.join('data', 'users.txt'), 'r') as file:
            users = file.readlines()
        exists = any("newuser|newpassword" in line for line in users)
        self.assertTrue(exists)
    # Story Creation Page Tests
    def test_story_creation_page_elements(self):
        """Test the presence and accessibility of critical elements on the Story Creation Page."""
        self.driver.get("http://localhost:5000/login")  # Redirect to login page to log in
        self.driver.find_element(By.ID, "username_field").send_keys("johndoe")
        self.driver.find_element(By.ID, "password_field").send_keys("password123")
        self.driver.find_element(By.ID, "login_button").click()
        
        time.sleep(1)

        assert self.driver.find_element(By.ID, "story_title_field")
        assert self.driver.find_element(By.ID, "story_content_field")
        assert self.driver.find_element(By.ID, "save_story_button")

    def test_story_creation_page_functionality(self):
        """Test the functionality of story creation."""
        self.driver.get("http://localhost:5000/login")  # Redirect to login page to log in
        self.driver.find_element(By.ID, "username_field").send_keys("johndoe")
        self.driver.find_element(By.ID, "password_field").send_keys("password123")
        self.driver.find_element(By.ID, "login_button").click()
        
        time.sleep(1)

        # Fill out the story creation form
        self.driver.find_element(By.ID, "story_title_field").send_keys("My New Story")
        self.driver.find_element(By.ID, "story_content_field").send_keys("This is the content of a new story.")
        self.driver.find_element(By.ID, "save_story_button").click()

        time.sleep(1)  # Wait for redirection
        self.assertIn("Create Your Story", self.driver.title)  # Expect to still be on the same page

        # Validate that the story details are stored correctly
        with open('data/stories.txt', 'r') as file:
            stories = file.readlines()
            assert "johndoe|My New Story|This is the content of a new story.\n" in stories
class TestDigitalStorytellingPlatform:
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
    py = r'C:\Users\84495\Desktop\asie-bench\codes\ChatDev-0\DigitalStorytellingPlatform\app.py'
    test = TestDigitalStorytellingPlatform(checker, py)
    print(test.main())


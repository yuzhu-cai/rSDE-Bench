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
    
    # Login Page Tests
    def test_login_elements(self):
        """Testing the integrity of elements on the Login Page."""
        self.assertTrue(self.driver.find_element(By.ID, 'login-form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'password').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'login-button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'register-link').is_displayed())
    
    def test_login_functionality(self):
        """Testing the functionality of Login Page."""
        self.assertIn("User Login", self.driver.title)
        username = "johndoe"
        password = "password123"
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, 'login-button').click()
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'register-link').click()
        self.assertIn("User Register", self.driver.title) 


    # Register Page Tests
    def test_register_elements(self):
        """Testing the integrity of elements on the Register Page."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'register-link').click()
        
        self.assertTrue(self.driver.find_element(By.ID, 'register-form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'password').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'register-button').is_displayed())

    def test_register_functionality(self):
        """Testing the functionality of Register Page."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'register-link').click()
        username = "tester"
        password = "testpassword"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.ID, 'register-button').click()

        with open(os.path.join("data", "users.txt"), "r") as file:
            users = file.readlines()
        self.assertIn(f"{username},{password}\n", users)

    # Home Page Tests
    def test_home_elements(self):
        """Testing the integrity of elements on the Home Page."""
        self.login()
        self.assertTrue(self.driver.find_element(By.ID, 'header').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'welcome-message').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'tips-link').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'resources-link').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'post-link').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'profile-button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'contact-button').is_displayed())

    def test_home_functionality(self):
        """Testing the functionality of Home Page."""
        self.login()
        self.assertIn("welcome", self.driver.find_element(By.ID, 'welcome-message').text.lower())

        self.driver.find_element(By.ID, 'tips-link').click()  # Visit Tips Page
        self.assertIn("Eco-Friendly Tips", self.driver.title)  # Verify redirection to Tips Page

        self.login()
        self.driver.find_element(By.ID, 'resources-link').click()  # Visit resources Page
        self.assertIn("Useful Resources", self.driver.title)  # Verify redirection to resources Page

        self.login()
        self.driver.find_element(By.ID, 'post-link').click()  # Visit Community Forum Page
        self.assertIn("Community Forum", self.driver.title)  # Verify redirection to Community Forum Page

        self.login()
        self.driver.find_element(By.ID, 'profile-button').click()  # Visit Profile Page
        self.assertIn("User Profile", self.driver.title)  # Verify redirection to Profile Page

        self.login()
        self.driver.find_element(By.ID, 'contact-button').click()  # Visit Contact Page
        self.assertIn("Contact Us", self.driver.title)  # Verify redirection to Contact Page

    # Tips Page Tests
    def test_tips_elements(self):
        """Testing the integrity of elements on the Eco-Friendly Tips Page."""
        self.login()
        self.driver.find_element(By.ID, 'tips-link').click()
        
        self.assertTrue(self.driver.find_element(By.ID, 'tips-list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add-tip-form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'tip-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'submit-tip-button').is_displayed())

    def test_tips_functionality(self):
        """Testing the functionality of Eco-Friendly Tips Page."""
        self.login()
        self.driver.find_element(By.ID, 'tips-link').click()
        
        tip_to_add = "Carry a reusable water bottle."
        self.driver.find_element(By.ID, 'tip-input').send_keys(tip_to_add)
        self.driver.find_element(By.ID, 'submit-tip-button').click()

        with open('data/tips.txt', 'r') as file:
            tips = file.readlines()
        self.assertIn(f"{tip_to_add}\n", tips)

        tips_list = self.driver.find_element(By.ID, 'tips-list').text
        for tip in tips:
            self.assertIn(tip.strip(), tips_list)

    # Resources Page Tests
    def test_resources_elements(self):
        """Testing the integrity of elements on the Resources Page."""
        self.login()
        self.driver.find_element(By.ID, 'resources-link').click()
        
        self.assertTrue(self.driver.find_element(By.ID, 'resources-list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'resource-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add-resource-button').is_displayed())

    def test_resources_functionality(self):
        """Testing the functionality of Resources Page."""
        self.login()
        self.driver.find_element(By.ID, 'resources-link').click()
        
        resource_to_add = "https://www.example.com"
        self.driver.find_element(By.ID, 'resource-input').send_keys(resource_to_add)
        self.driver.find_element(By.ID, 'add-resource-button').click()
        
        with open('data/resources.txt', 'r') as file:
            resources = file.readlines()
        self.assertIn(f"{resource_to_add}\n", resources)

        resources_list = self.driver.find_element(By.ID, 'resources-list').text
        for resource in resources:
            self.assertIn(resource.strip(), resources_list)

    # Forum Page Tests
    def test_forum_elements(self):
        """Testing the integrity of elements on the Community Forum Page."""
        self.login()
        self.driver.find_element(By.ID, 'post-link').click()  # This would normally bring us to the forum
        
        self.assertTrue(self.driver.find_element(By.ID, 'forum-posts').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'post-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'submit-post-button').is_displayed())

    def test_forum_functionality(self):
        """Testing the functionality of Community Forum Page."""
        self.login()
        self.driver.find_element(By.ID, 'post-link').click()
        
        post_to_add = "What are everyone's thoughts on electric vehicles?"
        self.driver.find_element(By.ID, 'post-input').send_keys(post_to_add)
        self.driver.find_element(By.ID, 'submit-post-button').click()
        
        with open('data/forum_posts.txt', 'r') as file:
            posts = file.readlines()
        self.assertIn(f"johndoe,{post_to_add}\n", posts)

    # Profile Page Tests
    def test_profile_elements(self):
        """Testing the integrity of elements on the Profile Page."""
        self.login()
        self.driver.find_element(By.ID, 'profile-button').click() 
        
        self.assertTrue(self.driver.find_element(By.ID, 'profile-info').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'username-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'update-profile-button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'logout-button').is_displayed())

    def test_profile_functionality(self):
        """Testing the functionality of Profile Page."""
        self.login()
        self.driver.find_element(By.ID, 'profile-button').click()

        # Assume we are changing the username and validating it
        previous_username = self.driver.find_element(By.ID, 'profile-info').text
        self.assertIn("johndoe", previous_username)

        new_username = "john_updated"
        self.driver.find_element(By.ID, 'username-input').clear()
        self.driver.find_element(By.ID, 'username-input').send_keys(new_username)
        self.driver.find_element(By.ID, 'update-profile-button').click()
        
        with open('data/users.txt', 'r') as file:
            users = file.readlines()
        self.assertIn(new_username, [user.split(',')[0] for user in users])  # Validate new username exists
        self.assertNotIn("johndoe", [user.split(',')[0] for user in users])  # Validate old username doed not exist

    # Contact Page Tests
    def test_contact_elements(self):
        """Testing the integrity of elements on the Contact Page."""
        self.login()
        self.driver.find_element(By.ID, 'contact-button').click()
        
        self.assertTrue(self.driver.find_element(By.ID, 'contact-form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'name-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'email-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'message-input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'send-button').is_displayed())

    def test_contact_functionality(self):
        """Testing the functionality of Contact Page."""
        self.login()
        self.driver.find_element(By.ID, 'contact-button').click()

        name = "John Doe"
        email = "johndoe@example.com"
        message = "Great website! I appreciate the resources."

        self.driver.find_element(By.ID, 'name-input').send_keys(name)
        self.driver.find_element(By.ID, 'email-input').send_keys(email)
        self.driver.find_element(By.ID, 'message-input').send_keys(message)
        self.driver.find_element(By.ID, 'send-button').click()
        with open('data/contact_messages.txt', 'r') as file:
            messages = file.readlines()
        
        self.assertIn(f"{name},{email},{message}\n", messages)  # Validate message is stored

class TestEcoFriendlyLivingTips:
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
            'total': 17,
            'total_basic': 9,
            'total_advanced': 8,
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-1\EcoFriendlyLivingTips\app.py'
    test = TestEcoFriendlyLivingTips(checker, py)
    print(test.main())
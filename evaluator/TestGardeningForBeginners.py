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
        username = "user1"
        password = "password1"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
    
    # Page 1: Login Page Tests
    def test_login_page_elements(self):
        """Test the presence of elements on the Login page."""

        # Check for the presence of key elements
        self.assertTrue(self.driver.find_element(By.ID, 'login_page').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'username_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'password_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'login_button').is_displayed())

    def test_login_functionality(self):
        """Test the functionality of the Login page."""
        self.assertIn("Login", self.driver.title)

        username = "user1"  # This should match an entry in users.txt
        password = "password1"  # This should match an entry in users.txt
        self.driver.find_element(By.ID, 'username_input').send_keys(username)
        self.driver.find_element(By.ID, 'password_input').send_keys(password)
        self.driver.find_element(By.ID, 'login_button').click()

        # Here, assume we have a method to verify login success
        self.assertIn("Gardening Tips", self.driver.title)

    # Page 2: Gardening Tips Tests
    def test_gardening_tips_page_elements(self):
        """Test the presence of elements on the Gardening Tips page."""
        self.login()
        
        # Check for the presence of key elements
        self.assertTrue(self.driver.find_element(By.ID, 'gardening_tips_page').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'tip_list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add_tip_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add_tip_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'refresh_tips_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'forum_button').is_displayed())

    def test_gardening_tips_functionality(self):
        """Test the functionality of the Gardening Tips page."""
        self.login()
        # Add a new tip
        new_tip = "Use a balanced fertilizer every month."
        self.driver.find_element(By.ID, 'add_tip_input').send_keys(new_tip)
        self.driver.find_element(By.ID, 'add_tip_button').click()

        # Verify that new tip is added
        self.driver.find_element(By.ID, 'refresh_tips_button').click()
        tip_list = self.driver.find_element(By.ID, 'tip_list').text
        self.assertIn(new_tip, tip_list)

        with open(os.path.join('data', 'tips.txt'), 'r') as file:
            tips = file.readlines()
        self.assertIn(f"{new_tip}\n", tips)
        for tip in tips:
            self.assertIn(tip.strip(), tip_list)
        
        self.login()
        self.driver.find_element(By.ID, 'forum_button').click()
        time.sleep(10)
        self.assertIn("Gardening Forum", self.driver.title)

    # Page 3: Gardening Forum Tests
    def test_forum_page_elements(self):
        """Test the presence of elements on the Forum page."""
        self.login()
        self.driver.find_element(By.ID, 'forum_button').click()

        # Check for the presence of key elements
        self.assertTrue(self.driver.find_element(By.ID, 'forum_page').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'post_comment_list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'new_post_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'new_post_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'refresh_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'comment_button_1').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'comment_input_1').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'comment_input_2').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'comment_button_2').is_displayed())

    def test_forum_functionality(self):
        """Test the functionality of the Forum page."""
        self.login()
        self.driver.find_element(By.ID, 'forum_button').click()

        # Read from forum_posts.txt file for comparison
        with open(os.path.join('data', 'forum_posts.txt'), 'r') as file:
            initial_posts = file.readlines()

        # Add a new post
        new_post = "What's the best time to water my plants?"
        self.driver.find_element(By.ID, 'new_post_input').send_keys(new_post)
        self.driver.find_element(By.ID, 'new_post_button').click()

        # Refresh the posts to verify the new post
        self.driver.find_element(By.ID, 'refresh_button').click()
        post_comment_list = self.driver.find_element(By.ID, 'post_comment_list').text
        self.assertIn(new_post, post_comment_list)
        with open(os.path.join('data', 'forum_posts.txt'), 'r') as file:
            forum_posts = file.readlines()
        self.assertIn(f"user1,{new_post},3\n", forum_posts)
        for forum_post in forum_posts:
            self.assertIn(forum_post.strip(), post_comment_list)
        
        # Add a new comment
        new_comment = "This is a test!"
        self.driver.find_element(By.ID, 'comment_input_1').send_keys(new_comment)
        self.driver.find_element(By.ID, 'comment_button_1').click()

        # Refresh the comments to verify the new comment
        self.driver.find_element(By.ID, 'refresh_button').click()
        post_comment_list = self.driver.find_element(By.ID, 'post_comment_list')
        self.assertIn(new_comment, post_comment_list)
        with open(os.path.join('data', 'comments.txt'), 'r') as file:
            comments = file.readlines()
        self.assertIn(f"1,user1,{new_post}\n", comments)
        for comment in comments:
            self.assertIn(comment.strip(), post_comment_list)

class TestGardeningForBeginners:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\GardeningForBeginners\app.py'
    test = TestGardeningForBeginners(checker, py)
    print(test.main())
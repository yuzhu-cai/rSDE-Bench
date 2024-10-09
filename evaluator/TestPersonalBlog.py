import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys
import time
from datetime import datetime

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the webdriver (assuming Chrome is being used)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")  # Start from the landing page

    def tearDown(self):
        self.driver.quit()  # Close the browser after each test

    def login(self):
        self.driver.delete_all_cookies()
        username = "john_doe"
        password = "password123"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    def test_login_elements(self):
        """Test the presence and accessibility of Login Page elements."""
        self.assertEqual(self.driver.title, "User Login")
        self.driver.find_element(By.ID, "username_input")
        self.driver.find_element(By.ID, "password_input")
        self.driver.find_element(By.ID, "login_button")
        self.driver.find_element(By.ID, "login_message")
        self.driver.find_element(By.ID, "register_link")

    def test_login_functionality(self):
        """Test Login Page functionality."""
        
        username = "john_doe"
        password = "password123"
        
        # Performing login
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

        # Check if redirected to Main Blog Page
        self.assertEqual(self.driver.title, "My Personal Blog")

        # Check if redirected to the User Registration Page by checking the title
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        self.assertEqual(self.driver.title, "User Registration")

    def test_registration_elements(self):
        """Test the presence and accessibility of Registration Page elements."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()

        self.driver.find_element(By.ID, "reg_username_input")
        self.driver.find_element(By.ID, "reg_password_input")
        self.driver.find_element(By.ID, "reg_email_input")
        self.driver.find_element(By.ID, "register_message")
        self.driver.find_element(By.ID, "register_button")

    def test_registration_functionality(self):
        """Test Registration Page functionality."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()

        # Registering a new user
        username = "newuser"
        password = "newpassword"
        email = "newuser@example.com"

        self.driver.find_element(By.ID, "reg_username_input").send_keys(username)
        self.driver.find_element(By.ID, "reg_password_input").send_keys(password)
        self.driver.find_element(By.ID, "reg_email_input").send_keys(email)
        self.driver.find_element(By.ID, "register_button").click()

        # Check if redirected to Main Blog Page
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertIn(f"{username},{password},{email}\n" in users)

    def test_main_blog_elements(self):
        """Test the presence and accessibility of Main Blog Page elements."""
        self.login()  # Ensure the user is logged in
        self.driver.find_element(By.ID, "blog_title")
        self.driver.find_element(By.ID, "new_post_button")
        self.driver.find_element(By.ID, "view_post_button")
        self.driver.find_element(By.ID, "post_list")
        self.driver.find_element(By.ID, "logout_button")
        self.driver.find_element(By.ID, "blog_message")

    def test_main_blog_functionality(self):
        """Test Main Blog Page functionality, e.g., New Post creation."""
        self.login()  # Ensure the user is logged in
        self.driver.find_element(By.ID, "new_post_button").click()
        self.assertEqual(self.driver.title, "Create New Post")
        time.sleep(1)

        self.login()  # Ensure the user is logged in

        self.driver.find_element(By.ID, "view_post_button").click()
        self.assertEqual(self.driver.title, "View Blog Post")
        time.sleep(1)

        self.login()  # Ensure the user is logged in
        self.driver.find_element(By.ID, "logout_button").click()
        self.assertEqual(self.driver.title, "User Login")
        time.sleep(1)

    def test_new_post_elements(self):
        """Test the presence and accessibility of New Post Page elements."""
        self.login()  # Ensure the user is logged in
        self.driver.find_element(By.ID, "new_post_button").click()

        self.driver.find_element(By.ID, "post_title_input")
        self.driver.find_element(By.ID, "post_content_area")
        self.driver.find_element(By.ID, "submit_post_button")
        self.driver.find_element(By.ID, "post_message")
    
    def test_new_post_functionality(self):
        """Test the presence and accessibility of New Post Page elements."""
        self.login()  # Ensure the user is logged in
        self.driver.find_element(By.ID, "new_post_button").click()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        title = f"Test Post Title {current_time}"
        content = f'This is the content for the test post {current_time}'
        # Fill the new post form
        self.driver.find_element(By.ID, "post_title_input").send_keys(title)
        self.driver.find_element(By.ID, "post_content_area").send_keys(content)
        self.driver.find_element(By.ID, "submit_post_button").click()

        # Verify if post is successfully created
        post_list = self.driver.find_element(By.ID, "post_list").text
        self.assertIn(title, post_list)

        with open(os.path.join('data', 'logs.txt'), 'r') as f:
            users = f.readlines()
            print(users)
            self.assertTrue(f"User john_doe created a new post titled '{title}'.\n" in users)
        
        with open(os.path.join('data', 'posts.txt'), 'r') as f:
            posts = f.readlines()
            self.assertTrue(f"{title}|{content}\n" in posts)
            # self.assertTrue(title in posts)
            # self.assertTrue(content in posts)

    def test_view_post_elements(self):
        """Test the presence and accessibility of View Post Page elements."""
        self.login()  # Ensure a post has been created
        self.driver.find_element(By.ID, "view_post_button").click()

        self.driver.find_element(By.ID, "view_post_title")
        self.driver.find_element(By.ID, "view_post_content")
        self.driver.find_element(By.ID, "edit_post_button")
        self.driver.find_element(By.ID, "delete_post_button")
        self.driver.find_element(By.ID, "back_to_blog_button")

    def test_view_post_functionality(self):
        """Test View Post Page functionality."""
        self.login()  # Ensure a post has been created
        self.driver.find_element(By.ID, "view_post_button").click()
        post_title = self.driver.find_element(By.ID, 'view_post_title').text
        post_content = self.driver.find_element(By.ID, 'view_post_content').text
        self.assertIn('Test Post Title', post_title)
        self.assertIn('This is the content for the test post', post_content)

        self.login()  # Ensure a post has been created
        self.driver.find_element(By.ID, "view_post_button").click()
        with open(os.path.join('data', 'posts.txt'), 'r') as f:
            posts_items = f.readlines()
        previous = len(posts_items)
        self.driver.find_element(By.ID, "delete_post_button").click()
        with open(os.path.join('data', 'posts.txt'), 'r') as f:
            posts_items = f.readlines()
        current = len(posts_items)
        self.assertEqual(previous - current, 1)

        self.login()  # Ensure a post has been created
        self.driver.find_element(By.ID, "view_post_button").click()
        self.driver.find_element(By.ID, "edit_post_button").click()
        self.assertEqual(self.driver.title, "Edit Blog Post")

        self.login()  # Ensure a post has been created
        self.driver.find_element(By.ID, "view_post_button").click()
        self.driver.find_element(By.ID, "back_to_blog_button").click()
        self.assertEqual(self.driver.title, "My Personal Blog")

    def test_edit_post_elements(self):
        """Test the presence and accessibility of Edit Post Page elements."""
        self.login()  # Ensure a post has been created
        self.driver.find_element(By.ID, "view_post_button").click()
        self.driver.find_element(By.ID, "edit_post_button").click()

        self.driver.find_element(By.ID, "post_title_input")
        self.driver.find_element(By.ID, "post_content_input")
        self.driver.find_element(By.ID, "submit_post_button")
        self.driver.find_element(By.ID, "back_to_blog_button")
    
    def test_edit_post_functionality(self):
        """Test the presence and accessibility of Edit Post Page elements."""
        self.login()  # Ensure a post has been created
        self.driver.find_element(By.ID, "view_post_button").click()
        self.driver.find_element(By.ID, "edit_post_button").click()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        title = f"Edit Post Title {current_time}"
        content = f'This is the content for the edit post {current_time}'
        # Fill the new post form
        previous_title = self.driver.find_element(By.ID, "post_title_input").get_attribute('value')
        self.driver.find_element(By.ID, "post_title_input").clear()
        self.driver.find_element(By.ID, "post_title_input").send_keys(title)
        previous_content = self.driver.find_element(By.ID, "post_content_input").get_attribute('value')
        self.driver.find_element(By.ID, "post_content_input").clear()
        self.driver.find_element(By.ID, "post_content_input").send_keys(content)
        self.driver.find_element(By.ID, "submit_post_button").click()
        
        with open(os.path.join('data', 'posts.txt'), 'r') as f:
            posts = f.readlines()
            self.assertTrue(title in posts)
            self.assertTrue(content in posts)

            self.assertTrue(previous_title not in posts)
            self.assertTrue(previous_content not in posts)

        self.driver.find_element(By.ID, "back_to_blog_button").click()
        self.assertEqual(self.driver.title, "My Personal Blog")

class TestPersonalBlog:
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
    py = r'/Users/caiyuzhu/Dev/asie-bench/codes/ChatDev-updating-3/PersonalBlog/app.py'
    test = TestPersonalBlog(checker, py)
    print(test.main())
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
        username = "username1"
        password = "password1"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "login_username").send_keys(username)
        self.driver.find_element(By.ID, "login_password").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_elements(self):
        self.driver.find_element(By.ID, 'login_username')
        self.driver.find_element(By.ID, 'login_password')
        self.driver.find_element(By.ID, 'login_button')
        self.driver.find_element(By.ID, 'login_error_message')
        self.driver.find_element(By.ID, 'link_register')

    def test_login_functionality(self):
        self.assertEqual(self.driver.title, "User Login")

        username = "username1"
        password = "password1"
        self.driver.find_element(By.ID, 'login_username').send_keys(username)
        self.driver.find_element(By.ID, 'login_password').send_keys(password)
        self.driver.find_element(By.ID, 'login_button').click()
        self.assertIn("User Portfolio", self.driver.title)  # Example expected title
        
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "link_register").click()
        self.assertEqual(self.driver.title, "User Registration")

    # Registration Page Tests
    def test_registration_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'link_register').click()
        self.driver.find_element(By.ID, 'reg_email')
        self.driver.find_element(By.ID, 'reg_username')
        self.driver.find_element(By.ID, 'reg_password')
        self.driver.find_element(By.ID, 'reg_button')

    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'link_register').click()
        email = "testuser@example.com"
        username = "newusername"
        password = "newpassword"
        self.driver.find_element(By.ID, 'reg_email').send_keys(email)
        self.driver.find_element(By.ID, 'reg_username').send_keys(username)
        self.driver.find_element(By.ID, 'reg_password').send_keys(password)
        self.driver.find_element(By.ID, 'reg_button').click()
        
        # Check if redirected to Main Blog Page
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username},{password},{email}\n" in users)

    # Portfolio Page Tests
    def test_portfolio_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'project_list')
        self.driver.find_element(By.ID, 'new_project_link')
        self.driver.find_element(By.ID, 'new_project_description')
        self.driver.find_element(By.ID, 'add_project_button')
        self.driver.find_element(By.ID, 'delete_project_button')
        self.driver.find_element(By.ID, 'blog_button')
        self.driver.find_element(By.ID, 'contact_button')

    def test_portfolio_functionality(self):
        self.login()
        
        project_link = "http://example.com/project"
        project_desc = "This is a test project"
        
        self.driver.find_element(By.ID, 'new_project_link').send_keys(project_link)
        self.driver.find_element(By.ID, 'new_project_description').send_keys(project_desc)
        self.driver.find_element(By.ID, 'add_project_button').click()
        project_list = self.driver.find_element(By.ID, 'project_list').text
        self.assertIn(project_link, project_list)
        self.assertIn(project_desc, project_list)

        with open(os.path.join('data', 'projects.txt'), 'r') as file:
            projects = file.readlines()
        self.assertIn(f"username1,{project_link},{project_desc}\n", projects)

        for project in projects:
            self.assertIn(project.split(',')[1], project_list)
        
        self.login()
        self.driver.find_element(By.ID, 'delete_project_button').click()
        with open(os.path.join('data', 'projects.txt'), 'r') as file:
            projects_after_delete = file.readlines()
        self.assertEqual(len(projects)-len(projects_after_delete), 1)

        self.login()
        self.driver.find_element(By.ID, 'blog_button').click()
        self.assertEqual(self.driver.title, "User Blog")

        self.login()
        self.driver.find_element(By.ID, 'contact_button').click()
        self.assertEqual(self.driver.title, "Contact Information")

    # Blog Page Tests
    def test_blog_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'blog_button').click()
        self.driver.find_element(By.ID, 'blog_posts')
        self.driver.find_element(By.ID, 'blog_title')
        self.driver.find_element(By.ID, 'blog_content')
        self.driver.find_element(By.ID, 'publish_blog_button')
        self.driver.find_element(By.ID, 'delete_blog_button')

    def test_blog_functionality(self):
        # Navigate to blog after login
        self.login()
        self.driver.find_element(By.ID, 'blog_button').click()
        
        blog_title = "My First Blog"
        blog_content = "This is the content of my first blog post."
        
        self.driver.find_element(By.ID, 'blog_title').send_keys(blog_title)
        self.driver.find_element(By.ID, 'blog_content').send_keys(blog_content)
        self.driver.find_element(By.ID, 'publish_blog_button').click()
        
        blog_posts = self.driver.find_element(By.ID, 'blog_posts').text
        self.assertIn(blog_title, blog_posts)
        self.assertIn(blog_content, blog_posts)

        with open(os.path.join('data', 'blogs.txt'), 'r') as file:
            blogs = file.readlines()
        self.assertIn(f"username1,{blog_title},{blog_content}\n", blogs)

        for blog in blogs:
            self.assertIn(blog.split(',')[1], blog_posts)
        
        self.login()
        self.driver.find_element(By.ID, 'blog_button').click()
        self.driver.find_element(By.ID, 'delete_blog_button').click()
        with open(os.path.join('data', 'blogs.txt'), 'r') as file:
            blogs_after_delete = file.readlines()
        self.assertEqual(len(blogs)-len(blogs_after_delete), 1)

    # Contact Page Tests
    def test_contact_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'contact_button').click()
        self.driver.find_element(By.ID, 'contact_name')
        self.driver.find_element(By.ID, 'contact_email')
        self.driver.find_element(By.ID, 'contact_message')
        self.driver.find_element(By.ID, 'send_message_button')

    def test_contact_functionality(self):
        # Navigate to contact page after login
        self.login()
        self.driver.find_element(By.ID, 'contact_button').click()
        
        contact_name = "User Name"
        contact_email = "user@example.com"
        message = "This is a test message."
        
        self.driver.find_element(By.ID, 'contact_name').send_keys(contact_name)
        self.driver.find_element(By.ID, 'contact_email').send_keys(contact_email)
        self.driver.find_element(By.ID, 'contact_message').send_keys(message)
        self.driver.find_element(By.ID, 'send_message_button').click()
        
        with open(os.path.join('data', 'contacts.txt'), 'r') as file:
            contacts = file.readlines()
        self.assertIn(f"{contact_name},{contact_email},{message}\n", contacts)

class TestPortfolioSite:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\PortfolioSite\app.py'
    test = TestPortfolioSite(checker, py)
    print(test.main())
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
    
    def test_login_elements(self):
        # Check the presence of critical elements on the Login page
        username_input = self.driver.find_element(By.ID, 'username-input')
        password_input = self.driver.find_element(By.ID, 'password-input')
        login_button = self.driver.find_element(By.ID, 'login-button')
        register_button = self.driver.find_element(By.ID, 'register-button')

        self.assertTrue(username_input.is_displayed())
        self.assertTrue(password_input.is_displayed())
        self.assertTrue(login_button.is_displayed())
        self.assertTrue(register_button.is_displayed())

    def test_login_functionality(self):
        self.assertIn("Login", self.driver.title)
        # Login using valid credentials from the data storage file
        username = "john_doe"
        password = "password123"
        self.driver.find_element(By.ID, 'username-input').send_keys(username)
        self.driver.find_element(By.ID, 'password-input').send_keys(password)
        self.driver.find_element(By.ID, 'login-button').click()
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'register-button').click()
        self.assertIn("Register", self.driver.title)

    def test_register_elements(self):
        # Navigate to the Register page
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'register-button').click()
        
        username_input = self.driver.find_element(By.ID, 'username-input')
        password_input = self.driver.find_element(By.ID, 'password-input')
        register_button = self.driver.find_element(By.ID, 'register-button')

        self.assertTrue(username_input.is_displayed())
        self.assertTrue(password_input.is_displayed())
        self.assertTrue(register_button.is_displayed())
    
    def test_register_functionality(self):
        # Navigate to the Register page
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'register-button').click()
        
        unique_username = "new_user"
        unique_password = "new_password"

        self.driver.find_element(By.ID, 'username-input').send_keys(unique_username)
        self.driver.find_element(By.ID, 'password-input').send_keys(unique_password)
        self.driver.find_element(By.ID, 'register-button').click()

        with open('data/users.txt', 'r') as file:
            users = file.readlines()
        self.assertIn(f"{unique_username},{unique_password}\n", users)

    def test_home_elements(self):
        self.login()

        # Check the presence of critical elements on the Home page
        welcome_message = self.driver.find_element(By.ID, 'welcome-message')
        forum_link = self.driver.find_element(By.ID, 'forum-link')
        post_advice_link = self.driver.find_element(By.ID, 'post-advice-link')
        my_account_link = self.driver.find_element(By.ID, 'my-account-link')
        contact_us_link = self.driver.find_element(By.ID, 'contact-us-link')
        recent_posts = self.driver.find_element(By.ID, 'recent-posts')

        self.assertTrue(welcome_message.is_displayed())
        self.assertTrue(forum_link.is_displayed())
        self.assertTrue(post_advice_link.is_displayed())
        self.assertTrue(my_account_link.is_displayed())
        self.assertTrue(contact_us_link.is_displayed())
        self.assertTrue(recent_posts.is_displayed())

    def test_home_functionality(self):
        # Login first
        self.login()
        
        welcome_message = self.driver.find_element(By.ID, 'welcome-message')
        self.assertIn("welcome", welcome_message.text.lower())

        recent_posts = self.driver.find_element(By.ID, 'recent-posts').text
        with open("data/advice_posts.txt", "r") as file:
            posts = file.readlines()
        titles = [line.split(",")[1].strip() for line in posts]
        contents = [line.split(",")[2].strip() for line in posts]
        for item in titles:
            self.assertIn(item, recent_posts)
        for item in contents:
            self.assertIn(item, recent_posts)
        
        self.driver.find_element(By.ID, 'forum-link').click()
        self.assertIn("Forum", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'post-advice-link').click()
        self.assertIn("Post Advice", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'my-account-link').click()
        self.assertIn("My Account", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'contact-us-link').click()
        self.assertIn("Contact Us", self.driver.title)

    
    def test_forum_elements(self):
        # Login first
        self.login()
        self.driver.find_element(By.ID, 'forum-link').click()
        
        # Check the presence of critical elements on the Forum page
        thread_list = self.driver.find_element(By.ID, 'thread-list')
        create_view_thread_button = self.driver.find_element(By.ID, 'view-thread-button')
        thread_title_input = self.driver.find_element(By.ID, 'thread-title-input')
        thread_content_area = self.driver.find_element(By.ID, 'thread-content-area')
        submit_thread_button = self.driver.find_element(By.ID, 'submit-thread-button')

        self.assertTrue(thread_list.is_displayed())
        self.assertTrue(create_view_thread_button.is_displayed())
        self.assertTrue(thread_title_input.is_displayed())
        self.assertTrue(thread_content_area.is_displayed())
        self.assertTrue(submit_thread_button.is_displayed())

    def test_forum_functionality(self):
        # Login first
        self.login()
        self.driver.find_element(By.ID, 'forum-link').click()

        # Create and submit a new thread
        thread_title = "Testing Thread Creation"
        thread_content = "This is a test thread."

        self.driver.find_element(By.ID, 'thread-title-input').send_keys(thread_title)
        self.driver.find_element(By.ID, 'thread-content-area').send_keys(thread_content)
        self.driver.find_element(By.ID, 'submit-thread-button').click()

        thread_list = self.driver.find_element(By.ID, 'thread-list')
        self.assertIn(thread_title, thread_list.text)

        with open("data/threads.txt", "r") as file:
            threads = file.readlines()
        self.assertIn(f"3,{thread_title},{thread_content},john_doe\n", threads)
        for item in threads:
            self.assertIn(item.split(",")[1].strip(), thread_list.text)
            self.assertIn(item.split(",")[2].strip(), thread_list.text)

        self.driver.find_element(By.ID, 'view-thread-button').click()
        self.assertIn("View Thread", self.driver.title)

    def test_view_thread_elements(self):
        # Login first, create a thread, then view it to test this functionality
        self.login()
        self.driver.find_element(By.ID, 'forum-link').click()
        self.driver.find_element(By.ID, 'view-thread-button').click()

        # Check the presence of critical elements on the View Thread page
        thread_title_display = self.driver.find_element(By.ID, 'view-thread-title')
        thread_content_display = self.driver.find_element(By.ID, 'view-thread-content')
        comments_section = self.driver.find_element(By.ID, 'comments-section')
        comment_input_area = self.driver.find_element(By.ID, 'comment-input-area')
        submit_comment_button = self.driver.find_element(By.ID, 'submit-comment-button')

        self.assertTrue(thread_title_display.is_displayed())
        self.assertTrue(thread_content_display.is_displayed())
        self.assertTrue(comments_section.is_displayed())
        self.assertTrue(comment_input_area.is_displayed())
        self.assertTrue(submit_comment_button.is_displayed())

    def test_view_thread_functionality(self):
        # Same as before: login, create a thread, and view it to test comments
        self.login()
        self.driver.find_element(By.ID, 'forum-link').click()
        self.driver.find_element(By.ID, 'view-thread-button').click()

        self.assertIn("Best Baby Names", self.driver.find_element(By.ID, 'view-thread-title').text)
        self.assertIn("Looking for unique baby name ideas!", self.driver.find_element(By.ID, 'view-thread-content').text)

        # Submit a comment to the thread
        comment_content = "Great thread!"
        self.driver.find_element(By.ID, 'comment-input-area').send_keys(comment_content)
        self.driver.find_element(By.ID, 'submit-comment-button').click()
        
        with open("data/comments.txt", "r") as file:
            comments = file.readlines()
        self.assertIn(f"3,1,{comment_content},john_doe\n", comments)

    def test_post_advice_elements(self):
        # Login first
        self.login()
        self.driver.find_element(By.ID, 'post-advice-link').click()
        
        # Check the presence of critical elements on the Post Advice page
        advice_title_input = self.driver.find_element(By.ID, 'advice-title-input')
        advice_content_area = self.driver.find_element(By.ID, 'advice-content-area')
        submit_advice_button = self.driver.find_element(By.ID, 'submit-advice-button')

        self.assertTrue(advice_title_input.is_displayed())
        self.assertTrue(advice_content_area.is_displayed())
        self.assertTrue(submit_advice_button.is_displayed())

    def test_post_advice_functionality(self):
        # Login first
        self.login()
        self.driver.find_element(By.ID, 'post-advice-link').click()

        # Post a new advice
        advice_title = "Advice on Sleep Training"
        advice_content = "Create a consistent bedtime routine."

        self.driver.find_element(By.ID, 'advice-title-input').send_keys(advice_title)
        self.driver.find_element(By.ID, 'advice-content-area').send_keys(advice_content)
        self.driver.find_element(By.ID, 'submit-advice-button').click()

        # Verify the advice was posted by checking the advice posts file
        with open('data/advice_posts.txt', 'r') as file:
            posts = file.readlines()
        self.assertIn(f"3,{advice_title},{advice_content},john_doe\n", posts)

    def test_my_account_elements(self):
        # Login first
        self.login()

        # Navigate to My Account page
        self.driver.find_element(By.ID, 'my-account-link').click()
        time.sleep(2)  # Wait for page to load

        # Check the presence of critical elements on the My Account page
        user_info_display = self.driver.find_element(By.ID, 'user-info-display')
        update_profile_button = self.driver.find_element(By.ID, 'update-profile-button')
        delete_account_button = self.driver.find_element(By.ID, 'delete-account-button')

        self.assertTrue(user_info_display.is_displayed())
        self.assertTrue(update_profile_button.is_displayed())
        self.assertTrue(delete_account_button.is_displayed())

    def test_my_account_functionality(self):
        # Login first
        self.login()

        # Navigate to My Account page
        self.driver.find_element(By.ID, 'my-account-link').click()
        time.sleep(2)  # Wait for page to load

        # Simulate updating profile or checking user info
        #user_info_display = self.driver.find_element(By.ID, 'user-info-display')
        
        self.driver.find_element(By.ID, 'user-info-display').send_keys("JohnDoe")
        self.driver.find_element(By.ID, 'update-profile-button').click()
        # Verify the advice was posted by checking the advice posts file
        with open('data/users.txt', 'r') as file:
            posts = file.readlines()
        self.assertIn("JohnDoe,password123\n", posts)
    def test_contact_us_elements(self):
        # Login first
        self.login()

        # Navigate to Contact Us page
        self.driver.find_element(By.ID, 'contact-us-link').click()
        time.sleep(2)  # Wait for page to load

        # Check the presence of critical elements on the Contact Us page
        contact_name_input = self.driver.find_element(By.ID, 'contact-name-input')
        contact_email_input = self.driver.find_element(By.ID, 'contact-email-input')
        contact_message_area = self.driver.find_element(By.ID, 'contact-message-area')
        send_message_button = self.driver.find_element(By.ID, 'send-message-button')
        #confirmation_message_display = self.driver.find_element(By.ID, 'confirmation-message')

        self.assertTrue(contact_name_input.is_displayed())
        self.assertTrue(contact_email_input.is_displayed())
        self.assertTrue(contact_message_area.is_displayed())
        self.assertTrue(send_message_button.is_displayed())
        #self.assertTrue(confirmation_message_display.is_displayed())
    
    def test_contact_us_functionality(self):
        # Login first
        self.login()

        # Navigate to Contact Us page
        self.driver.find_element(By.ID, 'contact-us-link').click()
        time.sleep(2)  # Wait for page to load

        # Simulate sending a message
        contact_name = "John Doe"
        contact_email = "john.doe@example.com"
        contact_message = "This is a test message."

        self.driver.find_element(By.ID, 'contact-name-input').send_keys(contact_name)
        self.driver.find_element(By.ID, 'contact-email-input').send_keys(contact_email)
        self.driver.find_element(By.ID, 'contact-message-area').send_keys(contact_message)
        self.driver.find_element(By.ID, 'send-message-button').click()

        # # Check that confirmation is displayed
        # time.sleep(2)  # Wait for form processing
        # confirmation_message = self.driver.find_element(By.ID, 'confirmation-message')
        # self.assertIn("Thank you", confirmation_message.text)
        with open('data/contact.txt', 'r') as file:
            posts = file.readlines()
        self.assertIn("3,John Doe,john.doe@example.com,This is a test message.,john_doe\n", posts) 

class TestParentingAdviceForum:
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-1\ParentingAdviceForum\app.py'
    test = TestParentingAdviceForum(checker, py)
    print(test.main())
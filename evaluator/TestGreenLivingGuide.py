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
        password = "password123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

    # Page 1: Login Tests
    def test_login_elements(self):
        self.driver.find_element(By.ID, "login-form")
        self.driver.find_element(By.ID, "username")
        self.driver.find_element(By.ID, "password")
        self.driver.find_element(By.ID, "login-button")
        self.driver.find_element(By.ID, "register-button")
        self.driver.find_element(By.ID, "error-message")

    def test_login_functionality(self):
        self.assertEqual(self.driver.title, "User Login")
        self.driver.find_element(By.ID, "username").send_keys("user1")
        self.driver.find_element(By.ID, "password").send_keys("password123")
        self.driver.find_element(By.ID, "login-button").click()
        self.assertIn("Home", self.driver.title)  # Example expected title

        self.driver.back()
        self.driver.find_element(By.ID, "register-button").click()
        self.assertEqual(self.driver.title, "User Register")

    # Page 2: Register Tests
    def test_register_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register-button").click()

        self.driver.find_element(By.ID, "register-form")
        self.driver.find_element(By.ID, "username")
        self.driver.find_element(By.ID, "password")
        self.driver.find_element(By.ID, "register-button")
        #self.driver.find_element(By.ID, "error-message")

    def test_register_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register-button").click()

        username = "newusername"
        password = "newpassword"

        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "register-button").click()
        
        # error_message = self.driver.find_element(By.ID, "error-message").text
        # self.assertEqual(error_message, "")

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
        self.assertTrue(f"{username},{password}\n" in users)

    # Page 3: Home Tests
    def test_home_elements(self):
        self.login()
        self.driver.find_element(By.ID, "welcome-message")
        self.driver.find_element(By.ID, "tips-section")
        self.driver.find_element(By.ID, "articles-section")
        self.driver.find_element(By.ID, "articles-link")
        self.driver.find_element(By.ID, "community-link")
        self.driver.find_element(By.ID, "explore-button")

    def test_home_functionality(self):
        self.login()
        welcome_message = self.driver.find_element(By.ID, "welcome-message").text
        self.assertIn("welcome", welcome_message.lower())
        
        tips_section = self.driver.find_element(By.ID, "tips-section").text
        with open('data/tips.txt') as f:
            tips_data = f.readlines()
        for tip in tips_data:
            self.assertIn(tip.split(":")[0].strip(), tips_section)
            self.assertIn(tip.split(":")[1].strip(), tips_section)
        
        articel_section = self.driver.find_element(By.ID, "articles-section").text
        with open('data/articles.txt') as f:
            articles_data = f.readlines()
        for article in articles_data:
            self.assertIn(article.split(":")[0], articel_section)
            #self.assertIn(article.split(":")[1], articel_section)

        self.login()
        self.driver.find_element(By.ID, "articles-link").click()
        self.assertEqual(self.driver.title, "Articles")

        self.login()
        self.driver.find_element(By.ID, "community-link").click()
        self.assertEqual(self.driver.title, "Community Forum")

        self.login()
        self.driver.find_element(By.ID, "explore-button").click()
        self.assertEqual(self.driver.title, "Green Tips")

    # Page 4: Tips Tests
    def test_tips_elements(self):
        self.login()
        self.driver.find_element(By.ID, "explore-button").click()
        
        self.driver.find_element(By.ID, "tips-list")
        self.driver.find_element(By.ID, "new-tip-form")
        self.driver.find_element(By.ID, "tip-title")
        self.driver.find_element(By.ID, "tip-description")
        self.driver.find_element(By.ID, "submit-tip-button")
        self.driver.find_element(By.ID, "success-message")

    def test_tips_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "explore-button").click()
        
        tip_title = "Save Water"
        tip_desc = "Take shorter showers."
        self.driver.find_element(By.ID, "tip-title").send_keys(tip_title)
        self.driver.find_element(By.ID, "tip-description").send_keys(tip_desc)
        self.driver.find_element(By.ID, "submit-tip-button").click()
        
        success_message = self.driver.find_element(By.ID, "success-message").text
        self.assertIn("succ", success_message.lower())

        tips_list = self.driver.find_element(By.ID, "tips-list").text
        with open('data/tips.txt') as f:
            tips_data = f.readlines()
        self.assertIn(f"{tip_title}:{tip_desc}\n", tips_data)

        for tip in tips_data:
            self.assertIn(tip.split(":")[0].strip(), tips_list)
            self.assertIn(tip.split(":")[1].strip(), tips_list)
    
    # Page 5: Articles Tests
    def test_articles_elements(self):
        self.login()
        self.driver.find_element(By.ID, "articles-link").click()

        self.driver.find_element(By.ID, "articles-list")
        self.driver.find_element(By.ID, "article-title")
        self.driver.find_element(By.ID, "article-content")
        self.driver.find_element(By.ID, "submit-article-button")

    def test_articles_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "articles-link").click()

        artical_title = "The Future of Renewable Energy"
        artical_content = "Renewable energy sources are the future..."
        self.driver.find_element(By.ID, "article-title").send_keys(artical_title)
        self.driver.find_element(By.ID, "article-content").send_keys(artical_content)
        self.driver.find_element(By.ID, "submit-article-button").click()

        articel_list = self.driver.find_element(By.ID, "articles-list").text
        with open('data/articles.txt') as f:
            articles_data = f.readlines()
        self.assertIn(f"{artical_title}:{artical_content}\n", articles_data)

        for article in articles_data:
            self.assertIn(article.split(":")[0], articel_list)
            #self.assertIn(article.split(",")[0], articel_list)

    # Page 6: Community Tests
    def test_community_elements(self):
        self.login()
        self.driver.find_element(By.ID, "community-link").click()

        self.driver.find_element(By.ID, "forum-posts")
        self.driver.find_element(By.ID, "new-post-form")
        self.driver.find_element(By.ID, "post-title")
        self.driver.find_element(By.ID, "post-content")
        self.driver.find_element(By.ID, "post-button")

    def test_community_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "community-link").click()

        post_title = "Sustainable Grocery Shopping"
        post_content = "Shop at local farmer's markets..."
        self.driver.find_element(By.ID, "post-title").send_keys(post_title)
        self.driver.find_element(By.ID, "post-content").send_keys(post_content)
        self.driver.find_element(By.ID, "post-button").click()
        
        post_section = self.driver.find_element(By.ID, "forum-posts").text
        with open('data/community_posts.txt') as f:
            posts_data = f.readlines()
        self.assertIn(f"{post_title}:{post_content}\n", posts_data)

        for post in posts_data:
            self.assertIn(post.split(":")[0], post_section)
            #self.assertIn(post.split(",")[0], post_section)

class TestGreenLivingGuide:
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-0\GreenLivingGuide\app.py'
    test = TestGreenLivingGuide(checker, py)
    print(test.main())
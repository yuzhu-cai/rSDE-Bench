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
        password = "securePassword123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
    
    # 1. Login Page Tests
    def test_login_page_elements(self):
        self.driver.find_element(By.ID, "username_field")
        self.driver.find_element(By.ID, "password_field")
        self.driver.find_element(By.ID, "login_button")
        self.driver.find_element(By.ID, "register_button")
        #self.driver.find_element(By.ID, "error_message")

    def test_login_page_functionality(self):
        self.assertEqual(self.driver.title, "Login")
        username = "john_doe"
        password = "securePassword123"
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
        self.assertIn("Home", self.driver.title)
        
        self.driver.delete_all_cookies()  
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()
        self.assertIn("Register", self.driver.title)

    # 2. Register Page Tests
    def test_register_page_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()

        self.driver.find_element(By.ID, "username_field")
        self.driver.find_element(By.ID, "password_field")
        self.driver.find_element(By.ID, "register_button")
        #self.driver.find_element(By.ID, "error_message")

    def test_register_page_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()

        username = "new_user"
        password = "newPassword123"
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "register_button").click()
        
        with open('data/users.txt', 'r') as f:
            users_data = f.readlines()
        self.assertIn(f"{username},{password}\n", users_data)  # Check if new user is registered

    # 3. Home Page Tests
    def test_home_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "manage_projects_button")
        self.driver.find_element(By.ID, "manage_profile_button")
        self.driver.find_element(By.ID, "welcome_message")
        self.driver.find_element(By.ID, "search_field")
        self.driver.find_element(By.ID, "search_button")
        self.driver.find_element(By.ID, "search_result")
        self.driver.find_element(By.ID, "featured_freelancers")
        self.driver.find_element(By.ID, "view_freelancer_details")

    def test_home_page_functionality(self):
        self.login()
        self.assertIn('welcom', self.driver.find_element(By.ID, "welcome_message").text.lower())

        free_name = "Jane Smith"
        self.driver.find_element(By.ID, "search_field").send_keys(free_name)
        self.driver.find_element(By.ID, "search_button").click()
        result = self.driver.find_element(By.ID, "search_result").text
        self.assertIn(free_name, result)

        free_feature = self.driver.find_element(By.ID, "featured_freelancers").text
        
        with open('data/freelancers.txt', 'r') as f:
            freelancers_data = f.readlines()
        names = [line.split(',')[0] for line in freelancers_data]
        links = [line.split(',')[2] for line in freelancers_data]
        for name in names:
            self.assertIn(name, free_feature)
        for link in links:
            self.assertIn(link, free_feature)
        
        self.driver.find_element(By.ID, "manage_projects_button").click()
        self.assertIn("Projects", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "manage_profile_button").click()
        self.assertIn("User Profile", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "view_freelancer_details").click()
        self.assertIn("Freelancer Profile", self.driver.title)

    # 4. Freelancer Profile Page Tests
    def test_freelancer_profile_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_freelancer_details").click()
        self.driver.find_element(By.ID, "freelancer_name")
        self.driver.find_element(By.ID, "information")
        

    def test_freelancer_profile_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_freelancer_details").click()
        information = self.driver.find_element(By.ID, "information").text
        
        with open('data/freelancers.txt', 'r') as f:
            freelancers_data = f.readlines()
        name = freelancers_data[0].split(',')[0].strip()
        email = freelancers_data[0].split(',')[1].strip()
        link = freelancers_data[0].split(',')[2].strip()


        self.assertIn(name, self.driver.find_element(By.ID, "freelancer_name").text)
        self.assertIn(email, information)
        self.assertIn(link, information)

    # 5. Project Listing Page Tests
    def test_project_listing_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "manage_projects_button").click()
        self.driver.find_element(By.ID, "pro_name")
        self.driver.find_element(By.ID, "pro_desc")
        self.driver.find_element(By.ID, "pro_fre_id")
        self.driver.find_element(By.ID, "create_project_button")
        self.driver.find_element(By.ID, "project_list")

    def test_project_listing_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "manage_projects_button").click()
        name = "New Project"
        desc = "A description for the new project."
        self.driver.find_element(By.ID, "pro_name").send_keys(name)
        self.driver.find_element(By.ID, "pro_desc").send_keys(desc)
        self.driver.find_element(By.ID, "pro_fre_id").send_keys("100")
        self.driver.find_element(By.ID, "create_project_button").click()
        
        with open('data/projects.txt', 'r') as f:
            projects_data = f.readlines()
        self.assertIn(f"{name},{desc},100\n", projects_data)

        project_list = self.driver.find_element(By.ID, "project_list").text
        with open('data/projects.txt', 'r') as f:
            projects_data = f.readlines()
        names = [line.split(',')[0] for line in projects_data]
        descs = [line.split(',')[1] for line in projects_data]
        ids = [line.split(',')[2] for line in projects_data]
        for name in names:
            self.assertIn(name, project_list)
        for desc in descs:
            self.assertIn(desc, project_list)
        for id in ids:
            self.assertIn(id, project_list)

    # 6. Profile Management Page Tests
    def test_profile_management_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "manage_profile_button").click()
        self.driver.find_element(By.ID, "user_name_field")
        self.driver.find_element(By.ID, "email_field")
        self.driver.find_element(By.ID, "update_profile_button")
        #self.driver.find_element(By.ID, "update_message")

    def test_profile_management_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "manage_profile_button").click()
        previous_name = self.driver.find_element(By.ID, "user_name_field").get_attribute("value")
        previous_email = self.driver.find_element(By.ID, "email_field").get_attribute("value")
        
        self.driver.find_element(By.ID, "user_name_field").clear()
        self.driver.find_element(By.ID, "user_name_field").send_keys("updated_user")
        self.driver.find_element(By.ID, "email_field").clear()
        self.driver.find_element(By.ID, "email_field").send_keys("updated_email@example.com")
        self.driver.find_element(By.ID, "update_profile_button").click()
        
        with open('data/users.txt', 'r') as f:
            users_data = f.readlines()
        self.assertIn("updated_user,", ''.join(users_data))
        #self.assertIn("updated_email@example.com,", ''.join(users_data))
        self.assertNotIn(previous_name, ''.join(users_data))
        self.assertNotIn(previous_email, ''.join(users_data))


class TestFreelancerMarketplace:
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-0\FreelancerMarketplace\app.py'
    test = TestFreelancerMarketplace(checker, py)
    print(test.main())
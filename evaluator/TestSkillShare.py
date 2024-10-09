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
        username = "johnDoe"
        password = "securePassword123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "usernameInput").send_keys(username)
        self.driver.find_element(By.ID, "passwordInput").send_keys(password)
        self.driver.find_element(By.ID, "loginButton").click()
    
        # Login Page Tests
    def test_login_elements(self):
        self.driver.find_element(By.ID, "usernameInput")
        self.driver.find_element(By.ID, "passwordInput")
        self.driver.find_element(By.ID, "loginButton")
        self.driver.find_element(By.ID, "registerButton")

    def test_login_functionality(self):
        username = "johnDoe"
        password = "securePassword123"
        self.driver.find_element(By.ID, "usernameInput").send_keys(username)
        self.driver.find_element(By.ID, "passwordInput").send_keys(password)
        self.driver.find_element(By.ID, "loginButton").click()
        self.assertIn("Dashboard", self.driver.title)

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "registerButton").click()
        self.assertIn("Register", self.driver.title)

    # Register Page Tests
    def test_register_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "registerButton").click()
        self.driver.find_element(By.ID, "usernameInput")
        self.driver.find_element(By.ID, "passwordInput")
        self.driver.find_element(By.ID, "registerButton")

    def test_register_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "registerButton").click()
        username = "newUser"
        password = "newPassword123"
        self.driver.find_element(By.ID, "usernameInput").send_keys(username)
        self.driver.find_element(By.ID, "passwordInput").send_keys(password)
        self.driver.find_element(By.ID, "registerButton").click()
        time.sleep(5)
        with open('data/users.txt', 'r') as f:
            users_data = f.readlines()
        self.assertIn(f"{username},{password}", "".join(users_data))  # Check if new user is registered

    # Dashboard Page Tests
    def test_dashboard_elements(self):
        self.login()
        self.driver.find_element(By.ID, "welcomeMessage")
        self.driver.find_element(By.ID, "featuredSkillsSection")
        self.driver.find_element(By.ID, "viewAllSkillsButton")
        self.driver.find_element(By.ID, "aboutButton")
        self.driver.find_element(By.ID, "profileLink")

    def test_dashboard_functionality(self):
        self.login()
        self.assertIn("welcom", self.driver.find_element(By.ID, "welcomeMessage").text.lower())
        skill_section = self.driver.find_element(By.ID, "featuredSkillsSection").text
        with open('data/skills.txt', 'r') as f:
            skills_data = f.readlines()
        # names = [line.split(':')[0] for line in skills_data]
        skills = [line.split(':')[1] for line in skills_data]
        # for name in names:
        #     self.assertIn(name, skill_section)
        for skill in skills:
            self.assertIn(skill, skill_section)

        self.driver.find_element(By.ID, "viewAllSkillsButton").click()
        self.assertIn("Skills", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "profileLink").click()
        self.assertIn("Profile", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "aboutButton").click()
        self.assertIn("About", self.driver.title)

    # Skills Page Tests
    def test_skills_elements(self):
        self.login()
        self.driver.find_element(By.ID, "viewAllSkillsButton").click()
        self.driver.find_element(By.ID, "skillsList")
        self.driver.find_element(By.ID, "newSkillInput")
        self.driver.find_element(By.ID, "addSkillButton")
        self.driver.find_element(By.ID, "removeSkillButton")

    def test_skills_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "viewAllSkillsButton").click()

        new_skill = "Testing"
        self.driver.find_element(By.ID, "newSkillInput").send_keys(new_skill)
        self.driver.find_element(By.ID, "addSkillButton").click()
        with open('data/skills.txt', 'r') as f:
            skills_ = f.read()
            self.assertIn("Testing", skills_)
            skills_data = f.readlines()
        names = [line.split(':')[0] for line in skills_data]
        skills = [line.split(':')[1] for line in skills_data]
        skill_list = self.driver.find_element(By.ID, "skillsList").text
        for name in names:
            self.assertIn(name, skill_list)
        for skill in skills:
            self.assertIn(skill, skill_list)

        self.driver.find_element(By.ID, "removeSkillButton").click()
        with open('data/skills.txt', 'r') as f:
            skills_data_del = f.readlines()
        self.assertEqual(len(skills_data)-len(skills_data_del), 1)

    # Profile Page Tests
    def test_profile_elements(self):
        self.login()
        self.driver.find_element(By.ID, "profileLink").click()
        self.driver.find_element(By.ID, "usernameInput")
        self.driver.find_element(By.ID, "saveChangesButton")

    def test_profile_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "profileLink").click()
        previous_name = self.driver.find_element(By.ID, "usernameInput").get_attribute("value")

        new_name = "johnDoeUpdated"
        self.driver.find_element(By.ID, "usernameInput").clear()
        self.driver.find_element(By.ID, "usernameInput").send_keys(new_name)
        self.driver.find_element(By.ID, "saveChangesButton").click()
        with open('data/profiles.txt', 'r') as f:
            profiles = f.read()
            self.assertIn(new_name, profiles)
            self.assertNotIn(previous_name, profiles)

    # About Page Tests
    def test_about_elements(self):
        self.login()
        self.driver.find_element(By.ID, "aboutButton").click()
        self.driver.find_element(By.ID, "aboutSection")
        self.driver.find_element(By.ID, "contactInfo")

    def test_about_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "aboutButton").click()
        info = self.driver.find_element(By.ID, "aboutSection").text
        contact = self.driver.find_element(By.ID, "contactInfo").text
        with open('data/about.txt', 'r') as f:
            abouts = f.readlines()
        about_info = abouts[0].split("|")[0].strip()
        about_contact = abouts[0].split("|")[1].strip()
        self.assertIn(about_info,info)
        self.assertIn(about_contact,contact)

class TestSkillShare:
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-0\SkillShare\app.py'
    test = TestSkillShare(checker, py)
    print(test.main())
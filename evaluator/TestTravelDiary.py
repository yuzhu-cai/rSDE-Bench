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
        password = "password1"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "inputUsername").send_keys(username)
        self.driver.find_element(By.ID, "inputPassword").send_keys(password)
        self.driver.find_element(By.ID, "btnLogin").click()

    def test_login_elements(self):
        # Check for presence of elements on the Login Page
        self.assertIsNotNone(self.driver.find_element(By.ID, 'inputUsername'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'inputPassword'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnLogin'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'linkRegister'))

    def test_login_functionality(self):
        self.assertIn("Login", self.driver.title)
        # Simulate login
        self.driver.find_element(By.ID, 'inputUsername').send_keys("john_doe")
        self.driver.find_element(By.ID, 'inputPassword').send_keys("password1")
        self.driver.find_element(By.ID, 'btnLogin').click()
        self.assertIn("Home", self.driver.title)  # Ensure we have navigated to the Home Page

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'linkRegister').click()
        self.assertIn("Register", self.driver.title)

    def test_registration_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'linkRegister').click()
        
        # Check for presence of elements on the Registration Page
        self.assertIsNotNone(self.driver.find_element(By.ID, 'inputUsername'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'inputPassword'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'inputEmail'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnRegister'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'linkLogin'))

    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'linkRegister').click()
        # Simulate registration
        self.driver.find_element(By.ID, 'inputUsername').send_keys("new_user")
        self.driver.find_element(By.ID, 'inputPassword').send_keys("new_password")
        self.driver.find_element(By.ID, 'inputEmail').send_keys("new_user@example.com")
        
        self.driver.find_element(By.ID, 'btnRegister').click()
        self.assertIn("Login", self.driver.title)  # Ensure we have navigated back to the Login Page

        with open(os.path.join("data", "users.txt"), 'r') as file:
            users = file.readlines()
        self.assertIn("new_user,new_password,new_user@example.com\n", users)

    def test_home_elements(self):
        self.login()

        self.assertIsNotNone(self.driver.find_element(By.ID, 'headerTitle'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnViewDiary'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnAddEntry'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnAbout'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'listEntries'))

    def test_home_functionality(self):
        self.login()
        listEntries = self.driver.find_element(By.ID, 'listEntries').text
        with open(os.path.join("data", "diary_entries.txt"), 'r') as file:
            diary_entries = file.readlines()
        titles = [line.split(",")[2].strip() for line in diary_entries]
        for title in titles:
            self.assertIn(title, listEntries)

        self.driver.find_element(By.ID, 'btnViewDiary').click()
        self.assertIn("View Diary", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'btnAddEntry').click()
        self.assertIn("Diary Entry", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'btnAbout').click()
        self.assertIn("About", self.driver.title)

    def test_diary_entry_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'btnAddEntry').click()
        
        # Check for presence of elements on the Diary Entry Page
        self.assertIsNotNone(self.driver.find_element(By.ID, 'inputEntryTitle'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'textareaEntry'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnSaveEntry'))

    def test_diary_entry_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'btnAddEntry').click()
        
        # Simulate entry addition
        self.driver.find_element(By.ID, 'inputEntryTitle').send_keys("Trip to Venice")
        self.driver.find_element(By.ID, 'textareaEntry').send_keys("Amazing experience in Venice.")
        self.driver.find_element(By.ID, 'btnSaveEntry').click()
        with open(os.path.join("data", "diary_entries.txt"), 'r') as file:
            diary_entries = file.readlines()
        self.assertIn("3,john_doe,Trip to Venice,Amazing experience in Venice.\n", diary_entries)

    def test_view_diary_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'btnViewDiary').click()
        
        # Check for presence of elements on the View Diary Page
        self.assertIsNotNone(self.driver.find_element(By.ID, 'listDiaryEntries'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnEdit'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnDelete'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnReturn'))

    def test_view_diary_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'btnViewDiary').click()
        
        listDiaryEntries = self.driver.find_element(By.ID, 'listDiaryEntries').text
        with open(os.path.join("data", "diary_entries.txt"), 'r') as file:
            diary_entries = file.readlines()
        titles = [line.split(",")[2].strip() for line in diary_entries]
        for title in titles:
            self.assertIn(title, listDiaryEntries)
        
        self.driver.find_element(By.ID, 'btnEdit').click()
        self.assertIn("Edit Diary Entry", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, 'btnViewDiary').click()
        self.driver.find_element(By.ID, 'btnDelete').click()
        with open(os.path.join("data", "diary_entries.txt"), 'r') as file:
            diary_entries = file.readlines()
        self.assertNotIn('1,john_doe,Trip to Paris,Had a wonderful time soaking in the sights...\n', diary_entries)

        self.driver.find_element(By.ID, 'btnReturn').click()
        self.assertIn("Home", self.driver.title)

    def test_edit_diary_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'btnViewDiary').click()
        self.driver.find_element(By.ID, 'btnEdit').click()
        
        # Check for presence of elements on the Edit Diary Entry Page
        self.assertIsNotNone(self.driver.find_element(By.ID, 'inputEntryTitle'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'textareaEntry'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'btnUpdateEntry'))

    def test_edit_diary_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'btnViewDiary').click()
        self.driver.find_element(By.ID, 'btnEdit').click()
        previous_title = self.driver.find_element(By.ID, 'inputEntryTitle').get_attribute("value")
        previous_content = self.driver.find_element(By.ID, 'textareaEntry').get_attribute("value")

        with open(os.path.join("data", "diary_entries.txt"), 'r') as file:
            diary_entries = file.readlines()
        titles = [line.split(",")[2].strip() for line in diary_entries]
        contents = [line.split(",")[3].strip() for line in diary_entries]
        self.assertIn(previous_title, titles)
        self.assertIn(previous_content, contents)

        self.driver.find_element(By.ID, 'inputEntryTitle').clear()
        self.driver.find_element(By.ID, 'inputEntryTitle').send_keys("Updated Trip to Venice")
        self.driver.find_element(By.ID, 'textareaEntry').clear()
        self.driver.find_element(By.ID, 'textareaEntry').send_keys("nice trip!")
        self.driver.find_element(By.ID, 'btnUpdateEntry').click()
        
        with open(os.path.join("data", "diary_entries.txt"), 'r') as file:
            diary_entries = file.readlines()
        titles = [line.split(",")[2].strip() for line in diary_entries]
        contents = [line.split(",")[3].strip() for line in diary_entries]
        self.assertIn("Updated Trip to Venice", titles)
        self.assertIn("nice trip!", contents)
        self.assertNotIn(previous_title, titles)
        self.assertNotIn(previous_content, contents)

    def test_about_elements(self):
        self.login()
        self.driver.find_element(By.ID, 'btnAbout').click()
        
        # Check for presence of elements on the About Page
        self.assertIsNotNone(self.driver.find_element(By.ID, 'headerTitle'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'contentInfo'))
        self.assertIsNotNone(self.driver.find_element(By.ID, 'linkContact'))

    def test_about_functionality(self):
        self.login()
        self.driver.find_element(By.ID, 'btnAbout').click()

        self.assertIsNotNone(self.driver.find_element(By.ID, 'headerTitle').text)
        self.assertIsNotNone(self.driver.find_element(By.ID, 'contentInfo').text)
        self.assertIsNotNone(self.driver.find_element(By.ID, 'linkContact').text)


class TestTravelDiary:
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
            'total': 15,
            'total_basic': 8,
            'total_advanced': 7,
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\TravelDiary\app.py'
    test = TestTravelDiary(checker, py)
    print(test.main())
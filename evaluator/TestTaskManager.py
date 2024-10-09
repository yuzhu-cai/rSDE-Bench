# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
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
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        self.driver.quit()


    def login(self):
        username = "johndoe"
        password = "password123"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'username_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'password_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'login_button').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'register_link').is_displayed())

    def test_login_page_functionality(self):
        driver = self.driver
        # Simulate login with valid credentials from data file
        username = 'johndoe'
        password = 'password123'
        
        driver.find_element(By.ID, 'username_input').send_keys(username)
        driver.find_element(By.ID, 'password_input').send_keys(password)
        driver.find_element(By.ID, 'login_button').click()
        
        # Verify we are on the Home Page now
        self.assertIn("Task Manager Home", driver.title)

    # Registration Page Tests
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'register_link').click()

        self.assertTrue(driver.find_element(By.ID, 'reg_username_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'reg_password_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'reg_email_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'register_button').is_displayed())

    def test_registration_page_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'register_link').click()

        # Register user
        driver.find_element(By.ID, 'reg_username_input').send_keys("newuser")
        driver.find_element(By.ID, 'reg_password_input').send_keys("newpass123")
        driver.find_element(By.ID, 'reg_email_input').send_keys("newuser@example.com")
        driver.find_element(By.ID, 'register_button').click()

        # Verify user registration by checking user data file
        with open(os.path.join('data', 'users.txt'), 'r') as file:
            users = file.readlines()
        exists = any("newuser|newpass123" in line for line in users)
        self.assertTrue(exists)

    # Home Page Tests
    def test_home_page_elements(self):
        driver = self.driver
        # Navigate to home page after logging in
        driver.find_element(By.ID, 'username_input').send_keys('johndoe')
        driver.find_element(By.ID, 'password_input').send_keys('password123')
        driver.find_element(By.ID, 'login_button').click()

        self.assertTrue(driver.find_element(By.ID, 'task_list').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'add_task_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'due_date_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'add_task_button').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'remove_task_button_1').is_displayed())
        # self.assertTrue(driver.find_element(By.ID, 'complete_task_button').is_displayed())
        # self.assertTrue(driver.find_element(By.ID, 'task_filter').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'back_to_login_button').is_displayed())

    def test_home_page_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, 'username_input').send_keys('johndoe')
        driver.find_element(By.ID, 'password_input').send_keys('password123')
        driver.find_element(By.ID, 'login_button').click()
        time.sleep(2)

        # Adding a task
        self.driver.find_element(By.ID, 'remove_task_button_1').click()

        time.sleep(2)

        # Verify task was saved in the data file
        with open(os.path.join('data', 'tasks.txt'), 'r') as file:
            tasks = file.readlines()
        task_removed = all("1|Finish project report|2023-10-31" not in line for line in tasks)
        self.assertTrue(task_removed)

        # Adding a task
        driver.find_element(By.ID, 'add_task_input').send_keys("New Task")
        driver.find_element(By.ID, 'due_date_input').send_keys("202309-12-01")
        driver.find_element(By.ID, 'add_task_button').click()
        time.sleep(2)

        # Verify task was saved in the data file
        with open(os.path.join('data', 'tasks.txt'), 'r') as file:
            tasks = file.readlines()
        task_added = any("3|New Task|202309-12-01" in line for line in tasks)
        self.assertTrue(task_added)

        # Adding a task
        self.driver.find_element(By.ID, 'back_to_login_button').click()

        self.assertEqual(self.driver.title, "Login")
        # Verify task was saved in the data file

class TestTaskManager:
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
    py = r'C:\Users\84495\Desktop\asie-bench\codes\gpt-4o-mini-0\TaskManager\app.py'
    test = TestTaskManager(checker, py)
    print(test.main())






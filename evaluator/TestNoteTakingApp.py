import os
import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):

    def setUp(self):
        # Initialize the web driver (make sure to provide the proper path for your web driver)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        # Close the browser session
        self.driver.quit()
    
    def login(self):
        self.driver.delete_all_cookies()
        username = "john_doe"
        password = "abcd1234hashed"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_elements(self):
        self.assertEqual(self.driver.title, "Login")
        self.driver.find_element(By.ID, "login_page")
        self.driver.find_element(By.ID, "username_field")
        self.driver.find_element(By.ID, "password_field")
        self.driver.find_element(By.ID, "login_button")
        self.driver.find_element(By.ID, "error_message")
        self.driver.find_element(By.ID, "register_link")

    def test_login_functionality(self):
        self.driver.find_element(By.ID, "username_field").send_keys("john_doe")
        self.driver.find_element(By.ID, "password_field").send_keys("abcd1234hashed")
        self.driver.find_element(By.ID, "login_button").click()
        self.assertIn("Dashboard", self.driver.title)

        # Check if redirected to the User Registration Page by checking the title
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        self.assertEqual(self.driver.title, "Register")

    # Registration Page Tests
    def test_registration_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        self.driver.find_element(By.ID, "registration_page")
        self.driver.find_element(By.ID, "register_username_field")
        self.driver.find_element(By.ID, "register_password_field")
        self.driver.find_element(By.ID, "confirm_password_field")
        self.driver.find_element(By.ID, "register_button")
        self.driver.find_element(By.ID, "registration_success_message")
        
    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        # Registering a new user
        username = "newuser"
        password = "newpassword"

        self.driver.find_element(By.ID, "register_username_field").send_keys(username)
        self.driver.find_element(By.ID, "register_password_field").send_keys(password)
        self.driver.find_element(By.ID, "confirm_password_field").send_keys(password)
        self.driver.find_element(By.ID, "register_button").click()

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username}:{password}\n" in users)

    # Dashboard Page Tests
    def test_dashboard_elements(self):
        self.login()
        self.driver.find_element(By.ID, "dashboard_page")
        self.driver.find_element(By.ID, "notes_list")
        self.driver.find_element(By.ID, "add_note_button")
        self.driver.find_element(By.ID, "view_note_button")
        self.driver.find_element(By.ID, "search_note_button")
        self.driver.find_element(By.ID, "logout_button")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_note_button").click()
        self.assertIn('Add Note', self.driver.title)
        
        self.login()
        notes_list = self.driver.find_element(By.ID, "notes_list").text
        with open(os.path.join('data', 'notes.txt'), 'r') as file:
            notes_ = file.readlines()
        notes = [line.split('|')[1].strip() for line in notes_]
        for note in notes:
            self.assertIn(note, notes_list)

        self.login()
        self.driver.find_element(By.ID, "view_note_button").click()
        self.assertIn("View Note", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "search_note_button").click()
        self.assertIn("Search Note", self.driver.title)

    # Add Note Page Tests
    def test_add_note_elements(self):
        self.login()
        self.driver.find_element(By.ID, "add_note_button").click()
        self.driver.find_element(By.ID, "add_note_page")
        self.driver.find_element(By.ID, "note_title_field")
        self.driver.find_element(By.ID, "note_content_field")
        self.driver.find_element(By.ID, "save_note_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_add_note_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_note_button").click()

        self.driver.find_element(By.ID, "note_title_field").send_keys("Another Test Note")
        self.driver.find_element(By.ID, "note_content_field").send_keys("This is yet another test note.")
        self.driver.find_element(By.ID, "save_note_button").click()
        with open(os.path.join('data', 'notes.txt'), 'r') as file:
            notes_ = file.readlines()
        notes = [line.split('|')[1].strip() for line in notes_]
        self.assertIn("Another Test Note", notes)
        self.login()
        notes_list = self.driver.find_element(By.ID, "notes_list").text
        self.assertIn("Another Test Note", notes_list)

        self.login()
        self.driver.find_element(By.ID, "add_note_button").click()
        self.driver.find_element(By.ID, "note_title_field").send_keys("Test cancel button Note")
        self.driver.find_element(By.ID, "note_content_field").send_keys("cancel button")
        self.driver.find_element(By.ID, "cancel_button").click()
        with open(os.path.join('data', 'notes.txt'), 'r') as file:
            notes_ = file.readlines()
        notes = [line.split('|')[1].strip() for line in notes_]
        self.assertNotIn("Test cancel button Note", notes)
        self.login()
        notes_list = self.driver.find_element(By.ID, "notes_list").text
        self.assertNotIn("Test cancel button Note", notes_list)

    # View Note Page Tests
    def test_view_note_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_note_button").click()
        self.driver.find_element(By.ID, "view_note_page")
        self.driver.find_element(By.ID, "note_title_field")
        self.driver.find_element(By.ID, "note_content_field")
        self.driver.find_element(By.ID, "edit_note_button")
        self.driver.find_element(By.ID, "delete_note_button")
        self.driver.find_element(By.ID, "back_to_dashboard_button")

    def test_view_note_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_note_button").click()
        title = "Grocery List"
        content = "Eggs, Milk, Bread"

        displayed_title = self.driver.find_element(By.ID, "note_title_field").get_attribute('value')
        displayed_content = self.driver.find_element(By.ID, "note_content_field").get_attribute('value')
        self.assertEqual(displayed_title, title)
        self.assertEqual(displayed_content, content)
        
        new_title = "new title"
        new_content = "new content"
        self.driver.find_element(By.ID, "note_title_field").clear()
        self.driver.find_element(By.ID, "note_title_field").send_keys(new_title)
        self.driver.find_element(By.ID, "note_content_field").clear()
        self.driver.find_element(By.ID, "note_content_field").send_keys(new_content)
        with open(os.path.join('data', 'notes.txt'), 'r') as file:
            notes_ = file.readlines()
        titles = [line.split('|')[1].strip() for line in notes_]
        contents = [line.split('|')[2].strip() for line in notes_]
        self.assertIn(new_title, titles)
        self.assertNotIn(displayed_title, titles)
        self.assertIn(new_content, contents)
        self.assertNotIn(displayed_content, contents)

        self.driver.find_element(By.ID, "back_to_dashboard_button").click()
        self.assertIn("Dashboard", self.driver.title)
        notes_list = self.driver.find_element(By.ID, "notes_list").text
        self.assertIn(new_title, notes_list)
        self.assertNotIn(title, notes_list)


    def test_search_note_elements(self):
        self.login()
        self.driver.find_element(By.ID, "search_note_button").click()
        self.driver.find_element(By.ID, "search_note_field")
        self.driver.find_element(By.ID, "search_note_button")
        self.driver.find_element(By.ID, "search_note_result")
        self.driver.find_element(By.ID, "back_button")

    def test_search_note_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "search_note_button").click()
        self.driver.find_element(By.ID, "search_note_field").send_keys("Meeting Notes")
        self.driver.find_element(By.ID, "search_note_button").click()
        result = self.driver.find_element(By.ID, "search_note_result").text
        self.assertIn("Meeting Notes", result)


class TestNoteTakingApp:
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-0\NoteTakingApp\app.py'
    test = TestNoteTakingApp(checker, py)
    print(test.main())
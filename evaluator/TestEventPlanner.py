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
        username = "john_doe"
        password = "abcd1234"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_elements(self):
        self.assertEqual(self.driver.title, "Login")
        self.driver.find_element(By.ID, "username_field")
        self.driver.find_element(By.ID, "password_field")
        self.driver.find_element(By.ID, "login_button")
        self.driver.find_element(By.ID, "error_message")
        self.driver.find_element(By.ID, "register_link")

    def test_login_functionality(self):
        self.driver.find_element(By.ID, "username_field").send_keys("john_doe")
        self.driver.find_element(By.ID, "password_field").send_keys("abcd1234")
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
        self.driver.find_element(By.ID, "events_list")
        self.driver.find_element(By.ID, "add_event_button")
        self.driver.find_element(By.ID, "search_event_button")
        self.driver.find_element(By.ID, "view_event_button")
        self.driver.find_element(By.ID, "logout_button")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_event_button").click()
        self.assertIn('Add Event', self.driver.title)
        
        self.login()
        events_list = self.driver.find_element(By.ID, "events_list").text
        with open(os.path.join('data', 'events.txt'), 'r') as file:
            events_ = file.readlines()
        events = [line.split('|')[1].strip() for line in events_]
        for event in events:
            self.assertIn(event, events_list)

        self.login()
        self.driver.find_element(By.ID, "view_event_button").click()
        self.assertIn("View Event", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "search_event_button").click()
        self.assertIn("Search Event", self.driver.title)

    # Add Note Page Tests
    def test_add_note_elements(self):
        self.login()
        self.driver.find_element(By.ID, "add_event_button").click()
        self.driver.find_element(By.ID, "event_title_field")
        self.driver.find_element(By.ID, "event_date_field")
        self.driver.find_element(By.ID, "event_location_field")
        self.driver.find_element(By.ID, "event_descriptionfield")
        self.driver.find_element(By.ID, "save_event_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_add_note_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "add_event_button").click()
        self.driver.find_element(By.ID, "event_title_field").send_keys("New Event")
        self.driver.find_element(By.ID, "event_date_field").send_keys("2000-01-01")
        self.driver.find_element(By.ID, "event_location_field").send_keys("New Location")
        self.driver.find_element(By.ID, "event_description_field").send_keys("This is a new event.")
        self.driver.find_element(By.ID, "save_event_button").click()
        with open(os.path.join('data', 'events.txt'), 'r') as file:
            notes_ = file.readlines()
        notes = [line.split('|')[1].strip() for line in notes_]
        self.assertIn("New Event", notes)
        notes = [line.split('|')[2].strip() for line in notes_]
        self.assertIn("2000-01-01", notes)
        notes = [line.split('|')[3].strip() for line in notes_]
        self.assertIn("New Location", notes)
        notes = [line.split('|')[4].strip() for line in notes_]
        self.assertIn("This is a new event.", notes)

        self.login()
        notes_list = self.driver.find_element(By.ID, "events_list").text
        self.assertIn("New Event", notes_list)

        self.login()
        self.driver.find_element(By.ID, "add_event_button").click()
        self.driver.find_element(By.ID, "event_title_field").send_keys("Test cancel button")
        self.driver.find_element(By.ID, "event_date_field").send_keys("2001-01-01")
        self.driver.find_element(By.ID, "event_location_field").send_keys("Test location")
        self.driver.find_element(By.ID, "event_description_field").send_keys("Test event")
        self.driver.find_element(By.ID, "cancel_button").click()
        with open(os.path.join('data', 'events.txt'), 'r') as file:
            notes_ = file.readlines()
        notes = [line.split('|')[1].strip() for line in notes_]
        self.assertNotIn("Test cancel button", notes)
        self.login()
        notes_list = self.driver.find_element(By.ID, "events_list").text
        self.assertNotIn("Test cancel button", notes_list)

    # View Note Page Tests
    def test_view_note_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_event_button").click()
        self.driver.find_element(By.ID, "event_title_field")
        self.driver.find_element(By.ID, "event_date_field")
        self.driver.find_element(By.ID, "event_location_field")
        self.driver.find_element(By.ID, "event_description_field")
        self.driver.find_element(By.ID, "edit_event_button")
        self.driver.find_element(By.ID, "delete_event_button")
        self.driver.find_element(By.ID, "back_to_dashboard_button")

    def test_view_note_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_event_button").click()
        expected_title = "Team Meeting"
        expected_date = "2024-08-30"
        expected_location = "Conference Room A"
        expected_description = "Discuss project updates."

        title_field = self.driver.find_element(By.ID, "event_title_field")
        displayed_title = title_field.get_attribute("value")
        displayed_date = self.driver.find_element(By.ID, "event_date_field").get_attribute("value")
        location_field = self.driver.find_element(By.ID, "event_location_field")
        displayed_location = location_field.get_attribute("value")
        displayed_description = self.driver.find_element(By.ID, "event_description_field").get_attribute("value")

        self.assertEqual(displayed_title, expected_title)
        self.assertEqual(displayed_date, expected_date)
        self.assertEqual(displayed_location, expected_location)
        self.assertEqual(displayed_description, expected_description)

        new_title = "Group Travel"
        new_location = "Airport"

        title_field.clear()
        title_field.send_keys(new_title)
        location_field.clear()
        location_field.send_keys(new_location)

        self.driver.find_element(By.ID, "edit_event_button").click()

        with open(os.path.join('data', 'events.txt'), 'r') as file:
            events = file.readlines()
        first_event = events[0].strip().split('|')
        self.assertEqual(first_event[1], new_title)
        self.assertEqual(first_event[2], expected_date)
        self.assertEqual(first_event[3], new_location)
        self.assertEqual(first_event[4], expected_description)

        self.driver.find_element(By.ID, "back_to_dashboard_button").click()
        self.assertIn("Dashboard", self.driver.title)
        notes_list = self.driver.find_element(By.ID, "events_list").text
        self.assertIn(new_title, notes_list)
        self.assertNotIn(expected_title, notes_list)


    def test_search_note_elements(self):
        self.login()
        self.driver.find_element(By.ID, "search_event_button").click()
        self.driver.find_element(By.ID, "search_event_field")
        self.driver.find_element(By.ID, "search_event_button")
        self.driver.find_element(By.ID, "search_event_result")
        self.driver.find_element(By.ID, "back_button")

    def test_search_note_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "search_event_button").click()
        self.driver.find_element(By.ID, "search_event_field").send_keys("Annual Conference")
        self.driver.find_element(By.ID, "search_event_button").click()
        result = self.driver.find_element(By.ID, "search_event_result").text
        self.assertIn("Annual Conference", result)


class TestEventPlanner:
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
    py = r'/Users/caiyuzhu/Dev/asie-bench/codes/ChatDev-0/EventPlanner/app.py'
    test = TestEventPlanner(checker, py)
    print(test.main())
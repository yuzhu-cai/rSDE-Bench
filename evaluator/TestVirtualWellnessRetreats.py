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

        # Check if redirected to the Registration Page by clicking the link
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
        self.driver.find_element(By.ID, "schedule_retreat_button")
        self.driver.find_element(By.ID, "view_bookings_button")
        self.driver.find_element(By.ID, "logout_button")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "schedule_retreat_button").click()
        self.assertIn('Schedule Retreat', self.driver.title)
        
        self.login()
        self.driver.find_element(By.ID, "view_bookings_button").click()
        self.assertIn("View Bookings", self.driver.title)

    # Schedule Retreat Page Tests
    def test_schedule_retreat_elements(self):
        self.login()
        self.driver.find_element(By.ID, "schedule_retreat_button").click()
        self.driver.find_element(By.ID, "retreat_title_field")
        self.driver.find_element(By.ID, "retreat_date_field")
        self.driver.find_element(By.ID, "retreat_time_field")
        self.driver.find_element(By.ID, "retreat_instructor_field")
        self.driver.find_element(By.ID, "schedule_retreat_button")
        self.driver.find_element(By.ID, "back_to_dashboard_button")

    def test_schedule_retreat_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "schedule_retreat_button").click()
        self.driver.find_element(By.ID, "retreat_title_field").send_keys("Night Yoga")
        self.driver.find_element(By.ID, "retreat_date_field").send_keys("202409-09-01")
        self.driver.find_element(By.ID, "retreat_time_field").send_keys("08:00 PM")
        self.driver.find_element(By.ID, "retreat_instructor_field").send_keys("Instructor A")
        self.driver.find_element(By.ID, "schedule_retreat_button").click()

        with open(os.path.join('data', 'retreats.txt'), 'r') as file:
            retreats = file.readlines()
        titles = [line.split('|')[2].strip() for line in retreats]
        self.assertIn("Night Yoga", titles)

        self.login()
        retreats_list = self.driver.find_element(By.ID, "retreats_list").text
        self.assertIn("Night Yoga", retreats_list)

    # View Bookings Page Tests
    def test_view_bookings_elements(self):
        self.login()
        self.driver.find_element(By.ID, "view_bookings_button").click()
        self.driver.find_element(By.ID, "booked_retreats_title")
        self.driver.find_element(By.ID, "booked_retreats_date")
        self.driver.find_element(By.ID, "booked_retreats_time")
        self.driver.find_element(By.ID, "booked_retreats_instructor")
        self.driver.find_element(By.ID, "retreat_title_field")
        self.driver.find_element(By.ID, "cancel_button")

    def test_view_bookings_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_bookings_button").click()

        expected_title = "Morning Yoga"
        expected_date = "2024-09-01"
        expected_time = "08:00 AM"
        expected_instructor = "Instructor A"

        # Check if the expected details are in the booked retreats before cancellation
        booked_titles = self.driver.find_element(By.ID, "booked_retreats_title").text
        booked_dates = self.driver.find_element(By.ID, "booked_retreats_date").text
        booked_times = self.driver.find_element(By.ID, "booked_retreats_time").text
        booked_instructors = self.driver.find_element(By.ID, "booked_retreats_instructor").text

        self.assertIn(expected_title, booked_titles)
        self.assertIn(expected_date, booked_dates)
        self.assertIn(expected_time, booked_times)
        self.assertIn(expected_instructor, booked_instructors)

        # Now cancel the booking
        title_field = self.driver.find_element(By.ID, "retreat_title_field")
        title_field.send_keys(expected_title)
        self.driver.find_element(By.ID, "cancel_button").click()

        # Verify that the retreat is removed from the file
        with open(os.path.join('data', 'retreats.txt'), 'r') as file:
            retreats = file.readlines()
        titles = [line.split('|')[2].strip() for line in retreats]
        self.assertNotIn(expected_title, titles)

        # Verify that the retreat is no longer listed in the booked retreats
        booked_titles = self.driver.find_element(By.ID, "booked_retreats_title").text
        self.assertNotIn(expected_title, booked_titles)



class TestVirtualWellnessRetreats:
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
            try:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\VirtualWellnessRetreats\app.py'
    test = TestVirtualWellnessRetreats(checker, py)
    print(test.main())

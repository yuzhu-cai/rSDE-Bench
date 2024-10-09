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
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
    
    # Login Page Tests
    def test_login_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "login_form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "username_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "login_button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "register_link").is_displayed())
    
    def test_login_functionality(self):
        self.assertIn("Login", self.driver.title)
        username = "john_doe"
        password = "password123"
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, 'login_button').click()
        self.assertIn("Home", self.driver.title)  # Verify redirection to Home Page

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, 'register_link').click()
        self.assertIn("Register", self.driver.title) 
        
    # Register Page Tests
    def test_register_page_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "register_form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "username_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "name_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "email_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "register_button").is_displayed())
    
    def test_register_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()

        username = "test_user"
        password = "test_password"
        name = "Test"
        email = "Test@email.com"
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "name_field").send_keys(name)
        self.driver.find_element(By.ID, "email_field").send_keys(email)
        self.driver.find_element(By.ID, "register_button").click()
        
        with open(os.path.join("data", "users.txt"), 'r') as file:
            users = file.readlines()
        self.assertIn(f"{username},{password},{name},{email}\n", users)
    
    # Homepage Tests
    def test_homepage_elements(self):
        self.login()
        self.assertTrue(self.driver.find_element(By.ID, "welcome_message").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "equipment_listing").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "promotions_section").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse_button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "help_button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my_rental_button").is_displayed())
    
    def test_homepage_functionality(self):
        self.login()
        self.assertIn("welcome", self.driver.find_element(By.ID, "welcome_message").text.lower())

        equipment_listing = self.driver.find_element(By.ID, "equipment_listing").text
        with open(os.path.join("data", "equipment.txt"), 'r') as file:
            equipment = file.readlines()
        names = [line.split(",")[1].strip() for line in equipment]
        for name in names:
            self.assertIn(name, equipment_listing)

        self.driver.find_element(By.ID, "browse_button").click()
        self.assertIn("Equipment", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "help_button").click()
        self.assertIn("Help", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "my_rental_button").click()
        self.assertIn("My Rentals", self.driver.title)
    
    # Equipment Page Tests
    def test_equipment_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "browse_button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "equipment_listing").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "show_details_button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "equipment_details").is_displayed())
        self.driver.find_element(By.ID, "rent_button")
    
    def test_equipment_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "browse_button").click()
        
        equipment_listing = self.driver.find_element(By.ID, "equipment_listing").text
        with open(os.path.join("data", "equipment.txt"), 'r') as file:
            equipment = file.readlines()
        names = [line.split(",")[1].strip() for line in equipment]
        for name in names:
            self.assertIn(name, equipment_listing)
        
        self.driver.find_element(By.ID, "show_details_button").click()
        equipment_details = self.driver.find_element(By.ID, "equipment_details").text
        details = equipment[0].split(",")
        for detail in details:
            self.assertIn(detail.strip(), equipment_details)
        
        self.driver.find_element(By.ID, "rent_button").click()
        self.assertIn("Rental Form", self.driver.title)
    
    # Rental Form Page Tests
    def test_rental_form_elements(self):
        self.login()
        self.driver.find_element(By.ID, "browse_button").click()
        self.driver.find_element(By.ID, "rent_button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "rental_form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "equipment_id_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rental_duration_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "user_details_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "submit_rental_button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rental_confirmation_msg").is_displayed())
    
    def test_rental_form_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "browse_button").click()
        self.driver.find_element(By.ID, "show_details_button").click()
        self.driver.find_element(By.ID, "rent_button").click()

        self.assertEqual(self.driver.find_element(By.ID, "equipment_id_field").text, "1")
        self.driver.find_element(By.ID, "rental_duration_field").send_keys("5")
        self.driver.find_element(By.ID, "user_details_field").send_keys("john_doe")
        self.driver.find_element(By.ID, "submit_rental_button").click()
        with open(os.path.join("data", "rentals.txt"), 'r') as file:
            rentals = file.readlines()
        self.assertIn("1004,john_doe,1,5,", rentals[-1])
        self.assertIn("active", rentals[-1])
        
        self.assertIsNotNone(self.driver.find_element(By.ID, "rental_confirmation_msg").text)
        
    # My Rentals Page Tests
    def test_my_rentals_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "my_rental_button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "my_current_rentals_listing").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "return_equipment_button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my_past_rentals_listing").is_displayed())
    
    def test_my_rentals_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "my_rental_button").click()

        with open(os.path.join("data", "rentals.txt"), 'r') as file:
            rentals = file.readlines()
        active = [line for line in rentals if line.split(",")[-1] == "activate"]
        inactive = [line for line in rentals if line.split(",")[-1] == "inactivate"]
        current_rentals = self.driver.find_element(By.ID, "my_current_rentals_listing").text
        past_rentals = self.driver.find_element(By.ID, "my_past_rentals_listing").text
        for item in active:
            ele = item.split(",")
            if ele[1] == 'john_doe':
                self.assertIn(ele[0], current_rentals)
                self.assertIn(ele[2], current_rentals)
                self.assertIn(ele[3], current_rentals)
                self.assertIn(ele[4], current_rentals)
            else:
                self.assertNotIn(ele[0], current_rentals)
                self.assertNotIn(ele[2], current_rentals)
                self.assertNotIn(ele[3], current_rentals)
                self.assertNotIn(ele[4], current_rentals)
        for item in inactive:
            ele = item.split(",")
            if ele[1] == 'john_doe':
                self.assertIn(ele[0], past_rentals)
                self.assertIn(ele[2], past_rentals)
                self.assertIn(ele[3], past_rentals)
                self.assertIn(ele[4], past_rentals)
            else:
                self.assertNotIn(ele[0], past_rentals)
                self.assertNotIn(ele[2], past_rentals)
                self.assertNotIn(ele[3], past_rentals)
                self.assertNotIn(ele[4], past_rentals)

        self.driver.find_element(By.ID, "return_equipment_button").click()
        self.assertIn("Return Equipment", self.driver.title)
    
    # Return Equipment Page Tests
    def test_return_equipment_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "my_rental_button").click()
        self.driver.find_element(By.ID, "return_equipment_button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "return_form").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "rental_id_field").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "confirm_return_button").is_displayed())
        self.driver.find_element(By.ID, "return_confirmation_msg")
    
    def test_return_equipment_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "my_rental_button").click()
        self.driver.find_element(By.ID, "return_equipment_button").click()
        
        self.driver.find_element(By.ID, "rental_id_field").send_keys("1003")  # example rental ID
        self.driver.find_element(By.ID, "confirm_return_button").click()
        
        with open(os.path.join("data", "returns.txt"), 'r') as file:
            returns = file.readlines()
        self.assertIn("5003,1003,", returns[-1])
        with open(os.path.join("data", "rentals.txt"), 'r') as file:
            rentals = file.readlines()
        self.assertNotIn('1003,john_doe,2,3,2023-10-09,active', rentals)
        self.assertIn('1003,john_doe,2,3,2023-10-09,inactive', rentals)
    
    # Help Page Tests
    def test_help_page_elements(self):
        self.login()
        self.driver.find_element(By.ID, "help_button").click()
        
        self.assertTrue(self.driver.find_element(By.ID, "faq_section").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "accessibility_info").is_displayed())
    
    def test_help_page_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "help_button").click()
        
        self.assertIsNotNone(self.driver.find_element(By.ID, "faq_section").text)
        self.assertIsNotNone(self.driver.find_element(By.ID, "accessibility_info").text)

class TestFitnessEquipmentRental:
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
    py = r'/Users/caiyuzhu/Dev/asie-bench/codes/ChatDev-updating-5/FitnessEquipmentRental/app.py'
    test = TestFitnessEquipmentRental(checker, py)
    print(test.main())
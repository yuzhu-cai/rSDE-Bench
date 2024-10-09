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
        self.driver.find_element(By.ID, "txt_username").send_keys("johndoe")
        self.driver.find_element(By.ID, "txt_password").send_keys("password123")
        self.driver.find_element(By.ID, "btn_login").click()
    # Login Page Tests
    def test_login_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "txt_username").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_password").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "btn_login").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "link_register").is_displayed())
    
    def test_login_functionality(self):
        self.driver.find_element(By.ID, "txt_username").send_keys("johndoe")
        self.driver.find_element(By.ID, "txt_password").send_keys("password123")
        self.driver.find_element(By.ID, "btn_login").click()
        self.assertIn("Dashboard", self.driver.title)

    # Registration Page Tests
    def test_registration_elements(self):
        self.driver.find_element(By.ID, "link_register").click()
        self.assertTrue(self.driver.find_element(By.ID, "txt_new_username").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_new_password").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "btn_register").is_displayed())
    
    def test_registration_functionality(self):
        self.driver.find_element(By.ID, "link_register").click()
        self.driver.find_element(By.ID, "txt_new_username").send_keys("newuser")
        self.driver.find_element(By.ID, "txt_new_password").send_keys("newpass")
        self.driver.find_element(By.ID, "txt_email").send_keys("newuser@example.com")
        self.driver.find_element(By.ID, "btn_register").click()

        # Verify user registration by checking user data file
        with open(os.path.join('data', 'users.txt'), 'r') as file:
            users = file.readlines()
        exists = any("newuser:newpass,newuser@example.com" in line for line in users)
        self.assertTrue(exists)
    #Dashboard Page Tests
    def test_dashboard_elements(self):
        self.login()  # Log in to reach the dashboard
        self.assertTrue(self.driver.find_element(By.ID, "btn_view_tutors").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "btn_request_tutoring").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "link_logout").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "link_profile").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "link_contact_us").is_displayed())
    
    def test_dashboard_functionality(self):
        self.login()  # Log in to reach the dashboard
        self.driver.find_element(By.ID, "btn_view_tutors").click()
        self.assertIn("Tutors", self.driver.title)  

    # Tutors Page Tests
    def test_tutors_elements(self):
        self.login()  # Navigate to dashboard first
        self.driver.find_element(By.ID, "btn_view_tutors").click()
        self.assertTrue(self.driver.find_element(By.ID, "div_tutor_list").is_displayed())
    
    def test_tutors_functionality(self):
        self.login()  # Navigate to dashboard first
        self.driver.find_element(By.ID, "btn_view_tutors").click()
        # Example functionality test: Verify if the tutor list is populated
        #self.assertGreater(len(self.driver.find_elements(By.CSS_SELECTOR, "#div_tutor_list > div")), 0)
        self.assertTrue(self.driver.find_element(By.ID, "div_tutor_list").is_displayed())

    # Request Tutoring Page Tests
    def test_request_tutoring_elements(self):
        self.login()  # Navigate to dashboard first
        self.driver.find_element(By.ID, "btn_request_tutoring").click()
        self.assertTrue(self.driver.find_element(By.ID, "txt_subject").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_details").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_date").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "btn_submit_request").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "link_cancel").is_displayed())
    
    def test_request_tutoring_functionality(self):
        self.login()  # Navigate to dashboard first
        self.driver.find_element(By.ID, "btn_request_tutoring").click()
        self.driver.find_element(By.ID, "txt_subject").send_keys("Math")
        self.driver.find_element(By.ID, "txt_details").send_keys("Need help with calculus.")
        self.driver.find_element(By.ID, "txt_date").send_keys("202309-12-01")
        time.sleep(10)

        self.driver.find_element(By.ID, "btn_submit_request").click()
        # Verify request is present in the requests data file
        with open('data/requests.txt') as f:
            requests = f.readlines()
        self.assertIn("johndoe:Math:Need help with calculus.:202309-12-01\n", requests)
    
    # Profile Page Tests
    def test_profile_elements(self):
        self.login()  # Log in to check profile
        self.driver.find_element(By.ID, "link_profile").click()
        self.assertTrue(self.driver.find_element(By.ID, "txt_username_display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_email_display").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "link_logout").is_displayed())
    
    def test_profile_functionality(self):
        self.login()  # Log in to check profile
        self.driver.find_element(By.ID, "link_profile").click()
        self.assertIn("johndoe", self.driver.find_element(By.ID, "txt_username_display").text)
        self.assertIn("johndoe@example.com", self.driver.find_element(By.ID, "txt_email_display").text)
    # Contact Us Page Tests
    def test_contact_us_elements(self):
        self.login()
        self.driver.find_element(By.ID, "link_contact_us").click()
        self.assertTrue(self.driver.find_element(By.ID, "txt_contact_name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_contact_email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "txt_contact_message").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "btn_send").is_displayed())
    
    def test_contact_us_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "link_contact_us").click()
        self.driver.find_element(By.ID, "txt_contact_name").send_keys("John Doe")
        self.driver.find_element(By.ID, "txt_contact_email").send_keys("johndoe@example.com")
        self.driver.find_element(By.ID, "txt_contact_message").send_keys("This is a test message.")
        self.driver.find_element(By.ID, "btn_send").click()
        time.sleep(1)
        # Verify message is present in the contact messages data file
        with open('data/contacts.txt') as f:
            contacts = f.readlines()
        self.assertIn("John Doe:johndoe@example.com:This is a test message.\n", contacts)

class TestPeerTutoringNetwork:
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
    py = r'C:\Users\84495\Desktop\asie-bench\codes\gpt-4o-mini-2\PeerTutoringNetwork\app.py'
    test = TestPeerTutoringNetwork(checker, py)
    print(test.main())






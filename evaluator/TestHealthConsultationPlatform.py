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

    #@classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
        self.driver.get("http://localhost:5000")

    #@classmethod
    def tearDown(self):
        self.driver.quit()

    def test_login_page_elements(self):
        driver = self.driver
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username_input')))

        self.assertTrue(driver.find_element(By.ID, 'username_field').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'password_field').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'login_button').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'register_link').is_displayed())

    def test_login_page_functionality(self):
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'username_input')))

        self.driver.find_element(By.ID, 'username_field').send_keys('username1')
        self.driver.find_element(By.ID, 'password_field').send_keys('password1')
        self.driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the page to load

        # Assuming successful login redirects to the Inquiry Page
        self.assertIn('Schedule Consultation', self.driver.title)

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
        exists = any("newuser,newpass123" in line for line in users)
        self.assertTrue(exists)


    def test_consultation_scheduling_page_elements(self):

        """Test to check for the integrity of the consultation scheduling page elements."""
        # self.test_login_page_functionality()  # Ensure we're logged in
        # self.driver.get(self.base_url + "/schedule")  # Navigate to scheduling page
        
        # Navigate to home page after logging in
        self.driver.find_element(By.ID, 'username_field').send_keys('username1')
        self.driver.find_element(By.ID, 'password_field').send_keys('password1')
        self.driver.find_element(By.ID, 'login_button').click()
        self.assertTrue(self.driver.find_element(By.ID, 'consultation_form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'date_field').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'time_slot_field').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'submit_schedule_button').is_displayed())
        

    def test_consultation_scheduling_page_functionality(self):
        """Test to verify scheduling functionality."""
        self.driver.find_element(By.ID, 'username_field').send_keys('username1')
        self.driver.find_element(By.ID, 'password_field').send_keys('password1')
        self.driver.find_element(By.ID, 'login_button').click()
        # Simulating scheduling
        self.driver.find_element(By.ID, 'date_field').send_keys('202309-10-20')
        self.driver.find_element(By.ID, 'time_slot_field').send_keys('10:00')  # Assuming available
        self.driver.find_element(By.ID, 'submit_schedule_button').click()

        # Verify confirmation message


        with open(os.path.join('data', 'consultations.txt'), 'r') as file:
            users = file.readlines()
        exists = any("username1,202309-10-20,10:00" in line for line in users)
        self.assertTrue(exists)


    def test_appointment_tracking_page_elements(self):
        """Test to check for the integrity of the appointment tracking page elements."""
        # self.test_login_page_functionality()  # Ensure we're logged in
        # self.driver.get(self.base_url + "/appointments")  # Navigate to appointments page
        self.driver.find_element(By.ID, 'username_field').send_keys('username1')
        self.driver.find_element(By.ID, 'password_field').send_keys('password1')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, "Tracking_Page_link").click()
        self.assertTrue(self.driver.find_element(By.ID, 'appointments_list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'feedback_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'logout_button').is_displayed())

    def test_appointment_tracking_page_functionality(self):
        """Test to verify appointment tracking functionality."""
        # self.test_login_page_functionality()  # Ensure we're logged in
        # self.driver.get(self.base_url + "/appointments")  # Navigate to appointments page
        
        # appointments_list = self.driver.find_element(By.ID, 'appointments_list')
        # self.assertTrue(appointments_list.is_displayed())
        # # Additional checks could be made here for the expected number of appointments
        self.driver.find_element(By.ID, 'username_field').send_keys('username1')
        self.driver.find_element(By.ID, 'password_field').send_keys('password1')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, "Tracking_Page_link").click()
        self.driver.find_element(By.ID, 'feedback_button').click()
        time.sleep(1)  # Wait for the page to load

        # Assuming successful login redirects to the Inquiry Page
        self.assertIn('Feedback', self.driver.title)
    def test_feedback_page_elements(self):
        """Test to check for the integrity of the feedback page elements."""
        # self.test_login_page_functionality()  # Ensure we're logged in
        # self.driver.get(self.base_url + "/feedback")  # Navigate to feedback page
        self.driver.find_element(By.ID, 'username_field').send_keys('username1')
        self.driver.find_element(By.ID, 'password_field').send_keys('password1')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, "Tracking_Page_link").click()
        self.driver.find_element(By.ID, 'feedback_button').click()
        self.assertTrue(self.driver.find_element(By.ID, 'feedback_form').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'feedback_textarea').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'submit_feedback_button').is_displayed())

    def test_feedback_page_functionality(self):
        """Test to verify feedback submission functionality."""
        # self.test_login_page_functionality()  # Ensure we're logged in
        # self.driver.get(self.base_url + "/feedback")  # Navigate to feedback page
        self.driver.find_element(By.ID, 'username_field').send_keys('username1')
        self.driver.find_element(By.ID, 'password_field').send_keys('password1')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, "Tracking_Page_link").click()
        self.driver.find_element(By.ID, 'feedback_button').click() 
        # Submit feedback
        self.driver.find_element(By.ID, 'feedback_textarea').send_keys('Excellent service!')
        self.driver.find_element(By.ID, 'submit_feedback_button').click()
        with open(os.path.join('data', 'feedback.txt'), 'r') as file:
            users = file.readlines()
        exists = any("username1,Excellent service!" in line for line in users)
        self.assertTrue(exists)
        # Ideally verify if the feedback submission was stored correctly, further checks can be implemented here.

    # @classmethod
    # def tearDownClass(cls):
    #     cls.driver.quit()


class TestHealthConsultationPlatform:
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
    py = r'C:\Users\84495\Desktop\asie-bench\codes\gpt-4o-mini-2\HealthConsultationPlatform\app.py'
    test = TestHealthConsultationPlatform(checker, py)
    print(test.main())
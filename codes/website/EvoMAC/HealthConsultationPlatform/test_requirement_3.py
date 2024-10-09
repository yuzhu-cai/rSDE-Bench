'''
Test the elements and integrity of all pages in the Health Consultation Platform.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class HealthConsultationPlatformTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)
    def test_login_page_elements(self):
        driver = self.driver
        # Check for Login Page Elements
        username_field = driver.find_element(By.ID, "username_field")
        password_field = driver.find_element(By.ID, "password_field")
        login_button = driver.find_element(By.ID, "login_button")
        register_link = driver.find_element(By.ID, "register_link")
        error_message = driver.find_element(By.ID, "error_message")
        self.assertIsNotNone(username_field)
        self.assertIsNotNone(password_field)
        self.assertIsNotNone(login_button)
        self.assertIsNotNone(register_link)
        self.assertIsNotNone(error_message)
    def test_registration_page_elements(self):
        driver = self.driver
        # Navigate to Registration Page
        driver.find_element(By.ID, "register_link").click()
        time.sleep(2)
        # Check for Registration Page Elements
        reg_username_input = driver.find_element(By.ID, "reg_username_input")
        reg_password_input = driver.find_element(By.ID, "reg_password_input")
        reg_email_input = driver.find_element(By.ID, "reg_email_input")
        register_button = driver.find_element(By.ID, "register_button")
        registration_success_message = driver.find_element(By.ID, "registration_success_message")
        self.assertIsNotNone(reg_username_input)
        self.assertIsNotNone(reg_password_input)
        self.assertIsNotNone(reg_email_input)
        self.assertIsNotNone(register_button)
        self.assertIsNotNone(registration_success_message)
    def test_consultation_scheduling_page_elements(self):
        driver = self.driver
        # Login to access Consultation Scheduling Page
        self.login("username1", "password1")  # Use valid credentials from users.txt
        time.sleep(2)
        # Check for Consultation Scheduling Page Elements
        consultation_form = driver.find_element(By.ID, "consultation_form")
        date_field = driver.find_element(By.ID, "date_field")
        time_slot_field = driver.find_element(By.ID, "time_slot_field")
        submit_schedule_button = driver.find_element(By.ID, "submit_schedule_button")
        tracking_page_link = driver.find_element(By.ID, "Tracking_Page_link")
        confirmation_message = driver.find_element(By.ID, "confirmation_message")
        self.assertIsNotNone(consultation_form)
        self.assertIsNotNone(date_field)
        self.assertIsNotNone(time_slot_field)
        self.assertIsNotNone(submit_schedule_button)
        self.assertIsNotNone(tracking_page_link)
        self.assertIsNotNone(confirmation_message)
    def test_appointment_tracking_page_elements(self):
        driver = self.driver
        # Login to access Appointment Tracking Page
        self.login("username1", "password1")  # Use valid credentials from users.txt
        time.sleep(2)
        # Navigate to My Appointments Page
        driver.find_element(By.ID, "Tracking_Page_link").click()
        time.sleep(2)
        # Check for Appointment Tracking Page Elements
        appointments_list = driver.find_element(By.ID, "appointments_list")
        feedback_button = driver.find_element(By.ID, "feedback_button")
        logout_button = driver.find_element(By.ID, "logout_button")
        self.assertIsNotNone(appointments_list)
        self.assertIsNotNone(feedback_button)
        self.assertIsNotNone(logout_button)
    def test_feedback_page_elements(self):
        driver = self.driver
        # Login to access Feedback Page
        self.login("username1", "password1")  # Use valid credentials from users.txt
        time.sleep(2)
        # Navigate to My Appointments Page
        driver.find_element(By.ID, "Tracking_Page_link").click()
        time.sleep(2)
        # Click on Leave Feedback
        driver.find_element(By.ID, "feedback_button").click()
        time.sleep(2)
        # Check for Feedback Page Elements
        feedback_form = driver.find_element(By.ID, "feedback_form")
        feedback_textarea = driver.find_element(By.ID, "feedback_textarea")
        submit_feedback_button = driver.find_element(By.ID, "submit_feedback_button")
        self.assertIsNotNone(feedback_form)
        self.assertIsNotNone(feedback_textarea)
        self.assertIsNotNone(submit_feedback_button)
    def login(self, username, password):
        driver = self.driver
        driver.find_element(By.ID, "username_field").send_keys(username)
        driver.find_element(By.ID, "password_field").send_keys(password)
        driver.find_element(By.ID, "login_button").click()
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
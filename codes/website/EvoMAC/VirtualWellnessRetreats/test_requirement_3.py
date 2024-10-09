'''
Test the elements and integrity of all pages in the VirtualWellnessRetreats application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestVirtualWellnessRetreats(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "john_doe"
        self.password = "abcd1234"
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'username_field'))
        self.assertTrue(driver.find_element(By.ID, 'password_field'))
        self.assertTrue(driver.find_element(By.ID, 'login_button'))
        self.assertTrue(driver.find_element(By.ID, 'error_message'))
        self.assertTrue(driver.find_element(By.ID, 'register_link'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'register_username_field'))
        self.assertTrue(driver.find_element(By.ID, 'register_password_field'))
        self.assertTrue(driver.find_element(By.ID, 'confirm_password_field'))
        self.assertTrue(driver.find_element(By.ID, 'register_button'))
        self.assertTrue(driver.find_element(By.ID, 'registration_success_message'))
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'schedule_retreat_button'))
        self.assertTrue(driver.find_element(By.ID, 'view_bookings_button'))
        self.assertTrue(driver.find_element(By.ID, 'logout_button'))
    def test_schedule_retreat_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'schedule_retreat_button').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'retreat_title_field'))
        self.assertTrue(driver.find_element(By.ID, 'retreat_date_field'))
        self.assertTrue(driver.find_element(By.ID, 'retreat_time_field'))
        self.assertTrue(driver.find_element(By.ID, 'retreat_instructor_field'))
        self.assertTrue(driver.find_element(By.ID, 'schedule_retreat_button'))
        self.assertTrue(driver.find_element(By.ID, 'back_to_dashboard_button'))
    def test_view_bookings_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'view_bookings_button').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'booked_retreats_title'))
        self.assertTrue(driver.find_element(By.ID, 'booked_retreats_date'))
        self.assertTrue(driver.find_element(By.ID, 'booked_retreats_time'))
        self.assertTrue(driver.find_element(By.ID, 'booked_retreats_instructor'))
        self.assertTrue(driver.find_element(By.ID, 'retreat_title_field'))
        self.assertTrue(driver.find_element(By.ID, 'cancel_button'))
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, 'username_field').send_keys(self.username)
        driver.find_element(By.ID, 'password_field').send_keys(self.password)
        driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the dashboard to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
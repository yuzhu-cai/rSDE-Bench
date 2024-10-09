'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestVolunteerMatchLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        # Verify that the current page is the login page
        self.assertIn("VolunteerMatch - Login", self.driver.title)
        login_form = self.driver.find_element(By.ID, "login-form")
        self.assertIsNotNone(login_form)
    def test_successful_login(self):
        # Attempt to log in with valid credentials
        username = "username1"  # Example username from data
        password = "password1"  # Example password from data
        username_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Verify that the user is redirected to the dashboard
        self.assertIn("VolunteerMatch - Dashboard", self.driver.title)
        dashboard_header = self.driver.find_element(By.ID, "dashboard-header")
        self.assertIsNotNone(dashboard_header)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
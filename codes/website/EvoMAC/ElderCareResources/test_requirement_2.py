'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestElderCareResourcesLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        # Check if the current page is the login page
        self.assertIn("User Login", self.driver.title)
        login_form = self.driver.find_element(By.ID, "login-form")
        self.assertIsNotNone(login_form)
    def test_login_functionality(self):
        # Attempt to log in with example data
        username = "john_doe"
        password = "password123"
        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if redirected to the dashboard page
        self.assertIn("Elder Care Resources Dashboard", self.driver.title)
        welcome_message = self.driver.find_element(By.ID, "welcome-message")
        self.assertEqual(welcome_message.text, "Welcome to ElderCareResources")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
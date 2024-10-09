'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestEcoFriendlyLivingTips(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Allow time for the page to load
    def test_login_page(self):
        # Verify that the current page is the login page
        self.assertIn("User Login", self.driver.title)
        login_form = self.driver.find_element(By.ID, "login-form")
        self.assertIsNotNone(login_form)
    def test_successful_login(self):
        # Attempt to log in with example data
        username = "johndoe"
        password = "password123"
        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(2)  # Allow time for the login process
        # Verify that we are redirected to the Home Page
        self.assertIn("Home", self.driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
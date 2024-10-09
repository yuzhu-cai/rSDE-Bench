'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.driver.implicitly_wait(10)
    def test_login_page_title(self):
        """Test if the first page is the login page."""
        self.assertIn("Login", self.driver.title)
    def test_successful_login(self):
        """Test if the login works with valid credentials."""
        username = "username1"  # Example username from data
        password = "password1"  # Example password from data
        # Locate the login form elements
        username_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        # Enter credentials and submit
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the page to load and check if redirected to Home Page
        time.sleep(2)  # Wait for the page to load
        self.assertIn("Home", self.driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
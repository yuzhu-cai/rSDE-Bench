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
        time.sleep(2)  # Wait for the page to load
    def test_login_page_title(self):
        """Test if the login page is displayed correctly."""
        self.assertIn("User Login", self.driver.title)
    def test_login_with_valid_credentials(self):
        """Test login functionality with valid credentials."""
        username = "john_doe"
        password = "password123"
        # Locate the login form elements
        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        # Input the credentials
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(2)  # Wait for the page to load after login
        # Check if redirected to the festival overview page
        self.assertIn("Online Cultural Festivals Overview", self.driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
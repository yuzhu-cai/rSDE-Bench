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
    def test_login_page_title(self):
        """Test if the login page is displayed correctly."""
        self.assertIn("User Login", self.driver.title)
    def test_login_with_valid_credentials(self):
        """Test login functionality with valid credentials."""
        username = "johndoe"
        password = "secret123"
        # Locate username and password input fields and login button
        username_input = self.driver.find_element(By.ID, "username_input")
        password_input = self.driver.find_element(By.ID, "password_input")
        login_button = self.driver.find_element(By.ID, "login_button")
        # Input username and password
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        # Wait for a moment to allow the page to load
        time.sleep(2)
        # Check if redirected to the Product Listing page
        self.assertIn("Product Listing", self.driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
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
        """Test if the login page title is correct."""
        self.assertIn("User Login", self.driver.title)
    def test_login_functionality(self):
        """Test if the login functionality works with valid credentials."""
        driver = self.driver
        # Locate the username and password fields
        username_field = driver.find_element(By.ID, "username_field")
        password_field = driver.find_element(By.ID, "password_field")
        login_button = driver.find_element(By.ID, "login_button")
        # Input valid credentials
        username_field.send_keys("johndoe")
        password_field.send_keys("password123")
        login_button.click()
        # Wait for redirection
        time.sleep(2)
        # Check if redirected to the Story Creation Page
        self.assertIn("Create Your Story", driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
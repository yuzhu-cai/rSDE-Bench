'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestOnlineVintageMarketLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        """Test if the first page is the login page."""
        title = self.driver.title
        self.assertIn("Login", title, "Login page title is incorrect.")
        # Check if login form is present
        login_form = self.driver.find_element(By.ID, "login-form")
        self.assertIsNotNone(login_form, "Login form is not present on the login page.")
    def test_login_functionality(self):
        """Test if the login functionality works with example data."""
        username = "johndoe"
        password = "password123"
        # Enter username
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys(username)
        # Enter password
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        # Click login button
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if redirected to home page
        home_title = self.driver.title
        self.assertIn("Home", home_title, "Login failed or did not redirect to home page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test whether the login page of the Nutrition Information Hub can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Check if the login page is accessible
        try:
            # Locate the username and password fields to ensure we are on the login page
            username_field = self.driver.find_element(By.ID, "usernameField")
            password_field = self.driver.find_element(By.ID, "passwordField")
            login_button = self.driver.find_element(By.ID, "loginButton")
            # Log the successful access to the login page
            print("Login page accessed successfully.")
            self.assertIsNotNone(username_field, "Username field is not found.")
            self.assertIsNotNone(password_field, "Password field is not found.")
            self.assertIsNotNone(login_button, "Login button is not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.fail("Login page access test failed.")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
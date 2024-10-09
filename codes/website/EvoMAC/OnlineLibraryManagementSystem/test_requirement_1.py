'''
Test whether the login page of the Online Library Management System can be accessed through the local port 5000.
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
            # Locate the login elements to ensure we are on the login page
            username_field = self.driver.find_element(By.ID, "login_username")
            password_field = self.driver.find_element(By.ID, "login_password")
            login_button = self.driver.find_element(By.ID, "login_button")
            register_button = self.driver.find_element(By.ID, "register_button")
            # Log the results
            print("Login page accessed successfully.")
            self.assertIsNotNone(username_field, "Username field is not found.")
            self.assertIsNotNone(password_field, "Password field is not found.")
            self.assertIsNotNone(login_button, "Login button is not found.")
            self.assertIsNotNone(register_button, "Register button is not found.")
        except Exception as e:
            print(f"Error accessing login page: {e}")
            self.fail("Login page could not be accessed.")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
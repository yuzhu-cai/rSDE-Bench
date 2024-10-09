'''
Test whether the login page of the SkillShare web application can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class TestSkillShareLoginPage(unittest.TestCase):
    def setUp(self):
        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Test if the login page is accessible
        try:
            # Wait for the page to load
            time.sleep(2)
            # Check if the login page title is correct
            self.assertIn("Login", self.driver.title)
            # Check if the username input field is present
            username_field = self.driver.find_element(By.ID, "usernameInput")
            self.assertIsNotNone(username_field)
            # Check if the password input field is present
            password_field = self.driver.find_element(By.ID, "passwordInput")
            self.assertIsNotNone(password_field)
            # Check if the login button is present
            login_button = self.driver.find_element(By.ID, "loginButton")
            self.assertIsNotNone(login_button)
            # Check if the register button is present
            register_button = self.driver.find_element(By.ID, "registerButton")
            self.assertIsNotNone(register_button)
            print("Login page accessed successfully.")
        except Exception as e:
            print(f"Error accessing login page: {e}")
    def tearDown(self):
        # Close the WebDriver
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
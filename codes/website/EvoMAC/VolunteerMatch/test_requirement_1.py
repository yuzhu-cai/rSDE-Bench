'''
Test whether the website can be accessed through local port 5000 and verify the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class TestVolunteerMatchLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Log the test case execution
        print("Testing access to the login page at http://localhost:5000")
        # Check if the login form is present
        try:
            login_form = self.driver.find_element(By.ID, "login-form")
            self.assertIsNotNone(login_form, "Login form should be present on the page.")
            print("Login form is present.")
        except Exception as e:
            print(f"Error occurred: {e}")
            self.fail("Login form not found on the login page.")
        # Check if username and password fields are present
        try:
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            self.assertIsNotNone(username_field, "Username field should be present.")
            self.assertIsNotNone(password_field, "Password field should be present.")
            print("Username and password fields are present.")
        except Exception as e:
            print(f"Error occurred: {e}")
            self.fail("Username or password field not found on the login page.")
        # Check if the login button is present
        try:
            login_button = self.driver.find_element(By.ID, "login-button")
            self.assertIsNotNone(login_button, "Login button should be present.")
            print("Login button is present.")
        except Exception as e:
            print(f"Error occurred: {e}")
            self.fail("Login button not found on the login page.")
    def tearDown(self):
        time.sleep(2)  # Wait for a bit before closing
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
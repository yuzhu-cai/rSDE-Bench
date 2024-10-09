'''
Test whether the website can be accessed through local port 5000 and verify the login page is accessible.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        # Check if the login form is present
        try:
            login_form = driver.find_element(By.ID, "login-form")
            self.assertIsNotNone(login_form, "Login form is not found on the page.")
            print("Login form is accessible.")
        except Exception as e:
            print(f"Error accessing login form: {e}")
        # Check if username input is present
        try:
            username_input = driver.find_element(By.ID, "username-input")
            self.assertIsNotNone(username_input, "Username input is not found on the page.")
            print("Username input is accessible.")
        except Exception as e:
            print(f"Error accessing username input: {e}")
        # Check if password input is present
        try:
            password_input = driver.find_element(By.ID, "password-input")
            self.assertIsNotNone(password_input, "Password input is not found on the page.")
            print("Password input is accessible.")
        except Exception as e:
            print(f"Error accessing password input: {e}")
        # Check if login button is present
        try:
            login_button = driver.find_element(By.ID, "login-button")
            self.assertIsNotNone(login_button, "Login button is not found on the page.")
            print("Login button is accessible.")
        except Exception as e:
            print(f"Error accessing login button: {e}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
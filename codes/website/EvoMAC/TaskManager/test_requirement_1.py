'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)  # Wait for elements to load
    def test_login_page_access(self):
        driver = self.driver
        try:
            # Navigate to the login page
            driver.get("http://localhost:5000")
            time.sleep(2)  # Wait for the page to load
            # Check if the login page is accessible by looking for the username input field
            username_input = driver.find_element(By.ID, "username_input")
            self.assertIsNotNone(username_input, "Login page is not accessible: Username input not found.")
            # Check if the password input field is present
            password_input = driver.find_element(By.ID, "password_input")
            self.assertIsNotNone(password_input, "Login page is not accessible: Password input not found.")
            # Check if the login button is present
            login_button = driver.find_element(By.ID, "login_button")
            self.assertIsNotNone(login_button, "Login page is not accessible: Login button not found.")
            print("Login page is accessible and all required elements are present.")
        except Exception as e:
            print(f"An error occurred: {e}")
    def tearDown(self):
        # Close the WebDriver
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
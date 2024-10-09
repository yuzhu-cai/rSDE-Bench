'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestGreenLivingGuideLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        # Check if the login form is present
        try:
            login_form = driver.find_element(By.ID, "login-form")
            self.assertIsNotNone(login_form, "Login form is not present on the page.")
            print("Login form is accessible.")
        except Exception as e:
            self.fail(f"Failed to access the login page: {str(e)}")
        # Check if the username and password fields are present
        try:
            username_field = driver.find_element(By.ID, "username")
            password_field = driver.find_element(By.ID, "password")
            self.assertIsNotNone(username_field, "Username field is not present.")
            self.assertIsNotNone(password_field, "Password field is not present.")
            print("Username and password fields are accessible.")
        except Exception as e:
            self.fail(f"Failed to find username/password fields: {str(e)}")
        # Attempt to log in with a valid user
        try:
            username_field.send_keys("user1")  # Example username from data storage
            password_field.send_keys("password123")  # Example password from data storage
            login_button = driver.find_element(By.ID, "login-button")
            login_button.click()
            time.sleep(2)  # Wait for the page to load
            # Check if redirected to Home page
            welcome_message = driver.find_element(By.ID, "welcome-message")
            self.assertIsNotNone(welcome_message, "Failed to redirect to Home page after login.")
            print("Successfully logged in and redirected to Home page.")
        except Exception as e:
            self.fail(f"Login failed or redirection issue: {str(e)}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
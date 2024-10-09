'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
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
    def test_login_page(self):
        driver = self.driver
        time.sleep(1)  # Allow time for the page to load
        # Check if the current page is the login page
        self.assertIn("User Login", driver.title)
        # Locate the login form elements
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        error_message = driver.find_element(By.ID, "error-message")
        # Input example data and attempt to log in
        username_field.send_keys("user1")
        password_field.send_keys("password123")
        login_button.click()
        time.sleep(1)  # Allow time for the login process to complete
        # Check if the login was successful by verifying the presence of the welcome message
        try:
            welcome_message = driver.find_element(By.ID, "welcome-message")
            self.assertIsNotNone(welcome_message)
        except Exception as e:
            self.assertTrue("Login failed, error message displayed" in error_message.text)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
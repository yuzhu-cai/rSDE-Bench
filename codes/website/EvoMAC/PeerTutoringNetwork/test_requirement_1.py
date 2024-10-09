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
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        # Check if the login page is accessible
        time.sleep(2)  # Wait for the page to load
        self.assertIn("Login", driver.title)  # Verify the title of the page
        username_input = driver.find_element(By.ID, "txt_username")
        password_input = driver.find_element(By.ID, "txt_password")
        login_button = driver.find_element(By.ID, "btn_login")
        # Check if the elements are present
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(password_input)
        self.assertIsNotNone(login_button)
        # Attempt to log in with valid credentials
        username_input.send_keys("johndoe")  # Example username
        password_input.send_keys("password123")  # Example password
        login_button.click()
        # Verify redirection to the dashboard page
        time.sleep(2)  # Wait for the page to load
        self.assertIn("Dashboard", driver.title)  # Verify that we are on the dashboard page
    def tearDown(self):
        # Close the WebDriver
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
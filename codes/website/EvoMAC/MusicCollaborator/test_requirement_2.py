'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        # Check if the current page is the login page
        self.assertIn("Login", self.driver.title)
        print("Login page is displayed correctly.")
        # Locate the username and password fields and the login button
        username_field = self.driver.find_element(By.ID, "usernameField")
        password_field = self.driver.find_element(By.ID, "passwordField")
        login_button = self.driver.find_element(By.ID, "loginButton")
        # Input example data and attempt to log in
        username_field.send_keys("john_doe")
        password_field.send_keys("password123")
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if the user is redirected to the Dashboard page
        self.assertIn("Dashboard", self.driver.title)
        print("User logged in successfully and redirected to the Dashboard page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestFitnessChallengesLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Wait for the page to load
    def test_login_page(self):
        driver = self.driver
        # Verify that the current page is the login page
        self.assertIn("User Login", driver.title)
        print("Login page title verified.")
        # Locate the login form elements
        username_field = driver.find_element(By.ID, "usernameField")
        password_field = driver.find_element(By.ID, "passwordField")
        login_button = driver.find_element(By.ID, "loginButton")
        # Input username and password from example data
        username = "johnsmith"
        password = "password123"
        # Perform login
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(2)  # Wait for the dashboard to load
        # Verify that the user is redirected to the dashboard
        self.assertIn("User Dashboard", driver.title)
        print("Successfully logged in and redirected to the dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestFitnessTrackerLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Wait for the page to load
    def test_login_page(self):
        # Check if the current page is the login page
        self.assertIn("Login", self.driver.title)
        print("Login page title verified.")
        # Locate the login elements
        username_field = self.driver.find_element(By.ID, "username_field")
        password_field = self.driver.find_element(By.ID, "password_field")
        login_button = self.driver.find_element(By.ID, "login_button")
        # Input example data for login
        username = "john_doe"
        password = "abcd1234"
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(2)  # Wait for the login process to complete
        # Verify that the user is redirected to the dashboard
        self.assertIn("Dashboard", self.driver.title)
        print("Login successful and redirected to Dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
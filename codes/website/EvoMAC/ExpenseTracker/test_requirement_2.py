'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestExpenseTrackerLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Wait for the page to load
    def test_login_page(self):
        # Check if the current page is the login page
        self.assertIn("User Login", self.driver.title)
        print("Login page title is correct.")
        # Check if the login form is present
        login_form = self.driver.find_element(By.ID, "login-form")
        self.assertIsNotNone(login_form)
        print("Login form is present.")
    def test_login_correct_credentials(self):
        # Input username and password
        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        username_input.send_keys("user1")  # Example username
        password_input.send_keys("pass123")  # Example password
        login_button.click()
        time.sleep(2)  # Wait for the dashboard to load
        # Check if redirected to the dashboard page
        self.assertIn("Expense Dashboard", self.driver.title)
        print("Successfully logged in and redirected to the dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
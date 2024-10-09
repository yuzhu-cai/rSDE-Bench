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
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("User Login", driver.title)
        print("Login page title is correct.")
        # Locate the username and password fields
        username_field = driver.find_element(By.ID, "usernameField")
        password_field = driver.find_element(By.ID, "passwordField")
        login_button = driver.find_element(By.ID, "loginButton")
        # Input the credentials from the example data
        username = "username1"
        password = "password1"
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if we are redirected to the home page
        self.assertIn("Home", driver.title)
        print("Successfully logged in and redirected to the home page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
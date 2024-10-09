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
        self.assertIn("Login", driver.title)
        print("Login page is displayed correctly.")
        # Locate the username and password fields and the login button
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "loginBtn")
        # Input example data for login
        username = "username1"  # Example username from data/users.txt
        password = "password1"  # Example password from data/users.txt
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the dashboard page to load
        time.sleep(2)
        # Check if redirected to the dashboard page
        self.assertIn("Dashboard", driver.title)
        print("Successfully logged in and redirected to the Dashboard page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
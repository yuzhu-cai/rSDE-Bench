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
        print("Login page title verified.")
        # Locate the username and password fields
        username_field = driver.find_element(By.ID, "login_username")
        password_field = driver.find_element(By.ID, "login_password")
        login_button = driver.find_element(By.ID, "login_button")
        # Input example data and attempt to log in
        username_field.send_keys("johndoe")
        password_field.send_keys("password123")
        login_button.click()
        # Wait for a moment to allow the page to load
        time.sleep(2)
        # Check if the user is redirected to the dashboard page
        self.assertIn("Dashboard", driver.title)
        print("Successfully logged in and redirected to the dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
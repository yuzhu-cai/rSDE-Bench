'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestNoteTakingApp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("Login", driver.title)
        print("Login page is displayed correctly.")
        # Locate the username and password fields
        username_field = driver.find_element(By.ID, "username_field")
        password_field = driver.find_element(By.ID, "password_field")
        login_button = driver.find_element(By.ID, "login_button")
        # Input example credentials
        username_field.send_keys("john_doe")
        password_field.send_keys("abcd1234")
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if redirected to the dashboard page
        self.assertIn("Dashboard", driver.title)
        print("Successfully logged in and redirected to the Dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
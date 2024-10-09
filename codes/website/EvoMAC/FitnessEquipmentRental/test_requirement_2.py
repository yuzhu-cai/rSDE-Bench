'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestFitnessEquipmentRental(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("Login", driver.title)
        print("Login page is displayed correctly.")
        # Locate the login form elements
        username_field = driver.find_element(By.ID, "username_field")
        password_field = driver.find_element(By.ID, "password_field")
        login_button = driver.find_element(By.ID, "login_button")
        # Input credentials from example data
        username = "john_doe"
        password = "password123"
        # Perform login
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if redirected to the homepage after login
        self.assertIn("Home", driver.title)
        print("Successfully logged in and redirected to the homepage.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
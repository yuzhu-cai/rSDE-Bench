'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestHealthConsultationPlatform(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("Login", driver.title)
        # Locate the username and password fields
        username_field = driver.find_element(By.ID, "username_field")
        password_field = driver.find_element(By.ID, "password_field")
        login_button = driver.find_element(By.ID, "login_button")
        # Input example data for login
        username = "username1"
        password = "password1"
        username_field.send_keys(username)
        password_field.send_keys(password)
        # Click the login button
        login_button.click()
        # Wait for a moment to allow redirection
        time.sleep(2)
        # Verify that the user is redirected to the Schedule Consultation page
        self.assertIn("Schedule Consultation", driver.title)
    def tearDown(self):
        # Close the browser window
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
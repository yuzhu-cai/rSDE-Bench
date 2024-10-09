'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestRemoteJobBoardLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("Login", driver.title)
        print("Login page is displayed correctly.")
        # Locate username and password fields
        username_input = driver.find_element(By.ID, "username-input")
        password_input = driver.find_element(By.ID, "password-input")
        login_button = driver.find_element(By.ID, "login-button")
        # Input example data from users.txt
        username = "john_doe"
        password = "password123"
        # Perform login
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if redirected to Home Page
        self.assertIn("Home", driver.title)
        print("Successfully logged in and redirected to Home page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
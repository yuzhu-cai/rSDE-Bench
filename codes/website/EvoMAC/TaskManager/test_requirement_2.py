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
        time.sleep(2)  # Wait for the page to load
    def test_login_page_title(self):
        """Test if the login page is displayed correctly."""
        self.assertIn("Login", self.driver.title)
        print("Login page title is correct.")
    def test_login_functionality(self):
        """Test if the login functionality works with valid credentials."""
        username = "johndoe"
        password = "password123"
        # Locate the username and password input fields
        username_input = self.driver.find_element(By.ID, "username_input")
        password_input = self.driver.find_element(By.ID, "password_input")
        login_button = self.driver.find_element(By.ID, "login_button")
        # Input the credentials
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(2)  # Wait for the login process to complete
        # Check if redirected to the home page
        self.assertIn("Task Manager Home", self.driver.title)
        print("Successfully logged in and redirected to the home page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
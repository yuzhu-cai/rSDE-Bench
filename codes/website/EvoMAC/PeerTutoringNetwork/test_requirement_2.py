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
        """Test if the first page is the login page."""
        self.assertIn("Login", self.driver.title)
        print("Login page title is correct.")
    def test_login_functionality(self):
        """Test if the login functionality works with example data."""
        username = "johndoe"
        password = "password123"
        # Locate the username and password fields and the login button
        username_field = self.driver.find_element(By.ID, "txt_username")
        password_field = self.driver.find_element(By.ID, "txt_password")
        login_button = self.driver.find_element(By.ID, "btn_login")
        # Input the username and password
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(2)  # Wait for the login process to complete
        # Check if redirected to the dashboard page
        self.assertIn("Dashboard", self.driver.title)
        print("Login functionality works correctly.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
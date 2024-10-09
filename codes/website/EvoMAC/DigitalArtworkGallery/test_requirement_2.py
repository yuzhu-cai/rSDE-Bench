'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_title(self):
        """Test if the login page is displayed correctly."""
        self.assertIn("Login", self.driver.title)
    def test_successful_login(self):
        """Test if the user can log in with valid credentials."""
        username = "john_doe"
        password = "abcd1234"
        # Locate the username and password fields
        username_field = self.driver.find_element(By.ID, "username_field")
        password_field = self.driver.find_element(By.ID, "password_field")
        login_button = self.driver.find_element(By.ID, "login_button")
        # Input the credentials
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Check if redirected to the gallery page
        self.assertIn("Gallery", self.driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
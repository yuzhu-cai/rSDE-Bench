'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Check if the login page is accessible
        time.sleep(2)  # Wait for the page to load
        self.assertIn("User Login", self.driver.title)  # Verify the title of the page
        # Check if the username field is present
        username_field = self.driver.find_element(By.ID, "username_field")
        self.assertIsNotNone(username_field)
        # Check if the password field is present
        password_field = self.driver.find_element(By.ID, "password_field")
        self.assertIsNotNone(password_field)
        # Check if the login button is present
        login_button = self.driver.find_element(By.ID, "login_button")
        self.assertIsNotNone(login_button)
        # Check if the register link is present
        register_link = self.driver.find_element(By.ID, "register_link")
        self.assertIsNotNone(register_link)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
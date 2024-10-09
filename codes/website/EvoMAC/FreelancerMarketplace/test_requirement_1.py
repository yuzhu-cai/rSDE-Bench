'''
Test whether the login page of the FreelancerMarketplace web application can be accessed through the local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Check if the login page is accessible
        time.sleep(2)  # Wait for the page to load
        self.assertIn("Login", self.driver.title)  # Verify the title contains 'Login'
        # Check if the login elements are present
        username_field = self.driver.find_element(By.ID, "username_field")
        password_field = self.driver.find_element(By.ID, "password_field")
        login_button = self.driver.find_element(By.ID, "login_button")
        register_button = self.driver.find_element(By.ID, "register_button")
        self.assertIsNotNone(username_field)
        self.assertIsNotNone(password_field)
        self.assertIsNotNone(login_button)
        self.assertIsNotNone(register_button)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
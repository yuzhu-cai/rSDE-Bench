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
        try:
            # Wait for the page to load
            time.sleep(2)
            # Locate the username and password fields
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            login_button = self.driver.find_element(By.ID, "loginBtn")
            registration_link = self.driver.find_element(By.ID, "registrationLink")
            about_link = self.driver.find_element(By.ID, "aboutLink")
            # Assert that the elements are present on the page
            self.assertIsNotNone(username_field, "Username field is not found.")
            self.assertIsNotNone(password_field, "Password field is not found.")
            self.assertIsNotNone(login_button, "Login button is not found.")
            self.assertIsNotNone(registration_link, "Registration link is not found.")
            self.assertIsNotNone(about_link, "About link is not found.")
            print("Login page accessed successfully and all elements are present.")
        except Exception as e:
            self.fail(f"Failed to access the login page: {str(e)}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
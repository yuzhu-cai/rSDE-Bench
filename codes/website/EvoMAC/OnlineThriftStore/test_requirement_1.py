'''
Test whether the login page of the OnlineThriftStore website can be accessed through the local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Check if the login page is accessible
        try:
            # Locate the username and password fields to confirm we are on the login page
            username_field = self.driver.find_element(By.ID, "username_field")
            password_field = self.driver.find_element(By.ID, "password_field")
            self.assertTrue(username_field.is_displayed(), "Username field is not displayed.")
            self.assertTrue(password_field.is_displayed(), "Password field is not displayed.")
            print("Login page accessed successfully.")
        except Exception as e:
            self.fail(f"Login page could not be accessed: {str(e)}")
    def tearDown(self):
        # Close the WebDriver
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
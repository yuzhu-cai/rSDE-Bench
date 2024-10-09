'''
Test whether the login page of the Music_Collaborator web application can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Log the test case execution
        logging.info("Testing access to the login page at http://localhost:5000")
        # Check if the login page is accessible by verifying the presence of the username field
        try:
            username_field = self.driver.find_element(By.ID, 'usernameField')
            self.assertIsNotNone(username_field, "Login page is not accessible: Username field not found.")
            logging.info("Login page is accessible: Username field found.")
        except Exception as e:
            logging.error(f"An error occurred while accessing the login page: {e}")
            self.fail("Login page is not accessible.")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
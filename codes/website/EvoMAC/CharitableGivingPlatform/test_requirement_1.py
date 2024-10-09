'''
Test whether the login page of the CharitableGivingPlatform can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
class TestCharitableGivingPlatform(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        logging.info("Testing access to the login page.")
        try:
            # Check if the login page is accessible by looking for the username input field
            username_input = self.driver.find_element(By.ID, "usernameInput")
            self.assertIsNotNone(username_input, "Login page is not accessible: username input not found.")
            logging.info("Login page accessed successfully.")
        except Exception as e:
            logging.error(f"Error accessing login page: {e}")
            self.fail("Failed to access the login page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
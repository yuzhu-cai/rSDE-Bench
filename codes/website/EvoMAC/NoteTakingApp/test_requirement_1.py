'''
Test whether the login page of the NoteTakingApp can be accessed through the local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        logging.info("Testing access to the login page.")
        try:
            # Check if the login page is accessible by looking for the username field
            username_field = self.driver.find_element(By.ID, "username_field")
            self.assertIsNotNone(username_field, "Login page is not accessible. Username field not found.")
            logging.info("Login page accessed successfully. Username field found.")
        except Exception as e:
            logging.error(f"Error accessing login page: {e}")
            self.fail("Failed to access the login page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
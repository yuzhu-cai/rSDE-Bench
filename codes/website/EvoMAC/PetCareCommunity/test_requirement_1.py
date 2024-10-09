'''
Test whether the website can be accessed through local port 5000, specifically checking the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
class TestPetCareCommunityLogin(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        logging.info("Testing access to the login page at http://localhost:5000")
        # Check if the login page is accessible
        try:
            login_page = self.driver.find_element(By.ID, "login-page")
            self.assertIsNotNone(login_page, "Login page is not accessible.")
            logging.info("Login page accessed successfully.")
        except Exception as e:
            logging.error(f"Error accessing login page: {e}")
            self.fail("Login page could not be accessed.")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
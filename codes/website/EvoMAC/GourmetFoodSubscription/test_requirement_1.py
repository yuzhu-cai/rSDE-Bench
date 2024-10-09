'''
Test whether the login page of the GourmetFoodSubscription web application can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
class TestGourmetFoodSubscriptionLogin(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        logging.info("Testing access to the login page.")
        # Check if the login page is accessible by looking for the username field
        try:
            username_field = self.driver.find_element(By.ID, 'username_field')
            self.assertIsNotNone(username_field, "Login page is not accessible. Username field not found.")
            logging.info("Login page accessed successfully. Username field found.")
        except Exception as e:
            logging.error(f"Error accessing login page: {e}")
            self.fail("Login page is not accessible.")
    def tearDown(self):
        # Close the browser window
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
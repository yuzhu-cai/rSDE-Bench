'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
class TestEventPlannerLoginPage(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        logging.info("Testing access to the login page at http://localhost:5000")
        # Check if the login page is accessible
        try:
            username_field = self.driver.find_element(By.ID, 'username_field')
            password_field = self.driver.find_element(By.ID, 'password_field')
            login_button = self.driver.find_element(By.ID, 'login_button')
            error_message = self.driver.find_element(By.ID, 'error_message')
            register_link = self.driver.find_element(By.ID, 'register_link')
            # Assert that the elements are present
            self.assertIsNotNone(username_field, "Username field is not found.")
            self.assertIsNotNone(password_field, "Password field is not found.")
            self.assertIsNotNone(login_button, "Login button is not found.")
            self.assertIsNotNone(error_message, "Error message area is not found.")
            self.assertIsNotNone(register_link, "Register link is not found.")
            logging.info("Login page elements are accessible.")
        except Exception as e:
            logging.error(f"Error accessing login page elements: {e}")
            self.fail("Login page elements could not be accessed.")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
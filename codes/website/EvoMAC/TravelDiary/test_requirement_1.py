'''
Test whether the login page of the TravelDiary website can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
class TestTravelDiaryLoginPage(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        logging.info("Testing access to the login page.")
        # Check if the login page is accessible
        try:
            username_field = self.driver.find_element(By.ID, "inputUsername")
            password_field = self.driver.find_element(By.ID, "inputPassword")
            login_button = self.driver.find_element(By.ID, "btnLogin")
            register_link = self.driver.find_element(By.ID, "linkRegister")
            # Verify that the elements are present on the page
            self.assertIsNotNone(username_field, "Username field is not found.")
            self.assertIsNotNone(password_field, "Password field is not found.")
            self.assertIsNotNone(login_button, "Login button is not found.")
            self.assertIsNotNone(register_link, "Register link is not found.")
            logging.info("Login page elements are accessible.")
        except Exception as e:
            logging.error(f"Error accessing login page: {e}")
            self.fail("Login page access test failed.")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
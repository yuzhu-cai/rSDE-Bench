'''
Test whether the website can be accessed through local port 5000, specifically the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        # Set up the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        # Wait for the page to load
        time.sleep(2)
        # Check if the login page is accessible by verifying the presence of the username input field
        try:
            username_input = driver.find_element(By.ID, "username-input")
            self.assertIsNotNone(username_input, "Login page is not accessible. Username input field not found.")
            print("Login page is accessible. Username input field found.")
        except Exception as e:
            self.fail(f"An error occurred while trying to access the login page: {str(e)}")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
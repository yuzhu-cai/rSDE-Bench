'''
Test whether the login page of the EcoFriendlyLivingTips web application can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        # Wait for the page to load
        time.sleep(2)
        # Check if the login form is present
        try:
            login_form = driver.find_element(By.ID, 'login-form')
            self.assertIsNotNone(login_form, "Login form is not found on the page.")
            print("Login page accessed successfully.")
        except Exception as e:
            print(f"Error accessing login page: {e}")
    def tearDown(self):
        # Close the browser window
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
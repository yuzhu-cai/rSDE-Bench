'''
Test whether the website can be accessed through local port 5000 and verify the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestExpenseTrackerLoginPage(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_access_login_page(self):
        driver = self.driver
        # Wait for the page to load
        time.sleep(2)
        # Check if the login form is present
        try:
            login_form = driver.find_element(By.ID, "login-form")
            self.assertIsNotNone(login_form, "Login form is not present on the page.")
            print("Login page accessed successfully.")
        except Exception as e:
            self.fail(f"Failed to access login page: {str(e)}")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        # Check if the login page is accessible by looking for the username input field
        try:
            username_input = driver.find_element(By.ID, "username_input")
            self.assertIsNotNone(username_input, "Login page is not accessible: Username input not found.")
            print("Login page is accessible: Username input found.")
        except Exception as e:
            self.fail(f"Login page is not accessible: {str(e)}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
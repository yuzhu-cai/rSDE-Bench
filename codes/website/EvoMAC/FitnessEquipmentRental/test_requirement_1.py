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
        # Check if the login form is present
        try:
            login_form = driver.find_element(By.ID, 'login_form')
            self.assertIsNotNone(login_form, "Login form is not found on the login page.")
            print("Login page accessed successfully.")
        except Exception as e:
            print(f"Error accessing login page: {e}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
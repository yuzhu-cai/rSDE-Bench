'''
Test whether the login page of the MotivationalQuotesApp can be accessed through local port 5000.
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
        # Wait for the page to load
        time.sleep(2)
        # Check if the login page is accessible by verifying the presence of the username input field
        try:
            username_input = self.driver.find_element(By.ID, "username_input")
            self.assertTrue(username_input.is_displayed(), "Login page is not accessible.")
            print("Login page accessed successfully.")
        except Exception as e:
            print(f"Error accessing login page: {e}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
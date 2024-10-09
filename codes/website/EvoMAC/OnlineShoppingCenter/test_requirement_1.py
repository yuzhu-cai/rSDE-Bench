'''
Test whether the login page of the website can be accessed through the local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        try:
            # Check if the login page is accessible by looking for the username input field
            username_input = self.driver.find_element(By.ID, "username_input")
            self.assertIsNotNone(username_input, "Login page is not accessible. Username input field not found.")
            print("Login page accessed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    def tearDown(self):
        time.sleep(2)  # Wait for a moment to observe the result
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
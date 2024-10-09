'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginFunctionality(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Allow time for the page to load
    def test_login_page(self):
        # Check if the current page is the login page
        self.assertIn("Login", self.driver.title)
        login_page_element = self.driver.find_element(By.ID, "login_page")
        self.assertIsNotNone(login_page_element)
    def test_login_correct_credentials(self):
        # Attempt to log in with correct credentials
        username = "user1"
        password = "password1"
        username_input = self.driver.find_element(By.ID, "username_input")
        password_input = self.driver.find_element(By.ID, "password_input")
        login_button = self.driver.find_element(By.ID, "login_button")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(2)  # Allow time for the login process to complete
        # Check if redirected to Gardening Tips page
        self.assertIn("Gardening Tips", self.driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
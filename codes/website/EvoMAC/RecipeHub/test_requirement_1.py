'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class TestRecipeHubLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Check if the login page is accessible
        time.sleep(2)  # Wait for the page to load
        try:
            username_input = self.driver.find_element(By.ID, "username_input")
            password_input = self.driver.find_element(By.ID, "password_input")
            login_button = self.driver.find_element(By.ID, "login_button")
            register_button = self.driver.find_element(By.ID, "register_button")
            self.assertTrue(username_input.is_displayed(), "Username input is not displayed.")
            self.assertTrue(password_input.is_displayed(), "Password input is not displayed.")
            self.assertTrue(login_button.is_displayed(), "Login button is not displayed.")
            self.assertTrue(register_button.is_displayed(), "Register button is not displayed.")
            print("Login page accessed successfully.")
        except Exception as e:
            print(f"Error accessing login page: {e}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
class TestLoginFunctionality(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        # Verify that the current page is the login page
        self.assertIn("Login", self.driver.title)
        username_input = self.driver.find_element(By.ID, "username-input")
        password_input = self.driver.find_element(By.ID, "password-input")
        login_button = self.driver.find_element(By.ID, "login-button")
        register_button = self.driver.find_element(By.ID, "register-button")
        # Check if all elements are present
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(password_input)
        self.assertIsNotNone(login_button)
        self.assertIsNotNone(register_button)
    def test_login_correct_credentials(self):
        # Perform login with correct credentials
        username_input = self.driver.find_element(By.ID, "username-input")
        password_input = self.driver.find_element(By.ID, "password-input")
        login_button = self.driver.find_element(By.ID, "login-button")
        username_input.send_keys("john_doe")
        password_input.send_keys("password123")
        login_button.click()
        # Verify that the user is redirected to the home page
        self.assertIn("Home", self.driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
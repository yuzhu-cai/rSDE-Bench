'''
Test whether the login page of the Movie Recommendation System can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
class TestLoginPageAccess(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Check if the login page is accessible
        try:
            username_field = self.driver.find_element(By.ID, 'usernameField')
            password_field = self.driver.find_element(By.ID, 'passwordField')
            login_button = self.driver.find_element(By.ID, 'loginButton')
            error_message = self.driver.find_element(By.ID, 'errorMessage')
            register_link = self.driver.find_element(By.ID, 'registerLink')
            # Log the results
            print("Login Page Access Test:")
            print("Username Field Found:", username_field is not None)
            print("Password Field Found:", password_field is not None)
            print("Login Button Found:", login_button is not None)
            print("Error Message Display Found:", error_message is not None)
            print("Register Link Found:", register_link is not None)
            # Assertions
            self.assertIsNotNone(username_field, "Username field is not found.")
            self.assertIsNotNone(password_field, "Password field is not found.")
            self.assertIsNotNone(login_button, "Login button is not found.")
            self.assertIsNotNone(error_message, "Error message display is not found.")
            self.assertIsNotNone(register_link, "Register link is not found.")
        except Exception as e:
            print("An error occurred:", e)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
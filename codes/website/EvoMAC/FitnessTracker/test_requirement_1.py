'''
Test whether the login page of the FitnessTracker web application can be accessed through local port 5000.
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
            username_field = self.driver.find_element(By.ID, "username_field")
            password_field = self.driver.find_element(By.ID, "password_field")
            login_button = self.driver.find_element(By.ID, "login_button")
            error_message = self.driver.find_element(By.ID, "error_message")
            register_link = self.driver.find_element(By.ID, "register_link")
            # Log the results
            print("Login Page Access Test: SUCCESS")
            print("Elements found on the login page:")
            print(f"Username Field: {username_field.is_displayed()}")
            print(f"Password Field: {password_field.is_displayed()}")
            print(f"Login Button: {login_button.is_displayed()}")
            print(f"Error Message Area: {error_message.is_displayed()}")
            print(f"Register Link: {register_link.is_displayed()}")
        except Exception as e:
            print("Login Page Access Test: FAILURE")
            print(f"Error encountered: {str(e)}")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
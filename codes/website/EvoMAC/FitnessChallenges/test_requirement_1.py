'''
Test whether the login page of the 'FitnessChallenges' web application can be accessed through local port 5000.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
class TestFitnessChallengesLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        # Check if the login page is accessible
        self.assertIn("User Login", self.driver.title)
        print("Login page accessed successfully.")
        # Check if the login form is present
        login_form = self.driver.find_element(By.ID, "loginForm")
        self.assertIsNotNone(login_form, "Login form is not present on the page.")
        print("Login form is present.")
        # Check if username and password fields are present
        username_field = self.driver.find_element(By.ID, "usernameField")
        password_field = self.driver.find_element(By.ID, "passwordField")
        self.assertIsNotNone(username_field, "Username field is not present.")
        self.assertIsNotNone(password_field, "Password field is not present.")
        print("Username and password fields are present.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
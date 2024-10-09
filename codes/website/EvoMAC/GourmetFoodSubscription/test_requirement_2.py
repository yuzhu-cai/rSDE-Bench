'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestGourmetFoodSubscriptionLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Allow time for the page to load
    def test_login_page(self):
        # Check if the current page is the login page
        self.assertIn("Login", self.driver.title)
        print("Login page title is correct.")
        # Check if the login elements are present
        username_field = self.driver.find_element(By.ID, "username_field")
        password_field = self.driver.find_element(By.ID, "password_field")
        login_button = self.driver.find_element(By.ID, "login_button")
        self.assertIsNotNone(username_field)
        self.assertIsNotNone(password_field)
        self.assertIsNotNone(login_button)
        print("Login elements are present on the page.")
    def test_login_correct_credentials(self):
        # Log in with correct credentials
        username = "john_doe"  # Example username from users.txt
        password = "abcd1234hashed"  # Example password from users.txt
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
        time.sleep(2)  # Allow time for the login process
        # Check if redirected to the dashboard
        self.assertIn("Dashboard", self.driver.title)
        print("Successfully logged in and redirected to the dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
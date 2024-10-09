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
    def test_login_page(self):
        # Check if the current page is the login page
        self.assertIn("User Login", self.driver.title)
        print("Login page title is correct.")
        # Check if the login elements are present
        username_input = self.driver.find_element(By.ID, "username_input")
        password_input = self.driver.find_element(By.ID, "password_input")
        login_button = self.driver.find_element(By.ID, "login_button")
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(password_input)
        self.assertIsNotNone(login_button)
        print("Login elements are present.")
    def test_login_correct_credentials(self):
        # Perform login with correct credentials
        self.driver.find_element(By.ID, "username_input").send_keys("john_doe")
        self.driver.find_element(By.ID, "password_input").send_keys("password123")
        self.driver.find_element(By.ID, "login_button").click()
        time.sleep(2)  # Wait for the page to load
        # Check if redirected to the main blog page
        self.assertIn("My Personal Blog", self.driver.title)
        print("Successfully logged in and redirected to the main blog page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
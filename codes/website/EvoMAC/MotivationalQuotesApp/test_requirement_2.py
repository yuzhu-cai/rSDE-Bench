'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("Login", driver.title, "Login page title is incorrect.")
        # Check if the login elements are present
        username_input = driver.find_element(By.ID, "username_input")
        password_input = driver.find_element(By.ID, "password_input")
        login_button = driver.find_element(By.ID, "login_button")
        self.assertIsNotNone(username_input, "Username input field is missing.")
        self.assertIsNotNone(password_input, "Password input field is missing.")
        self.assertIsNotNone(login_button, "Login button is missing.")
    def test_login_functionality(self):
        driver = self.driver
        # Perform login with example data
        username = "user1"
        password = "abc123"
        driver.find_element(By.ID, "username_input").send_keys(username)
        driver.find_element(By.ID, "password_input").send_keys(password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(2)  # Wait for the page to load
        # Check if redirected to home page
        self.assertIn("Home", driver.title, "Login failed or did not redirect to home page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
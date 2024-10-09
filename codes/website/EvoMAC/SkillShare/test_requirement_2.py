'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestSkillShareLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("Login", driver.title)
        print("Login page is displayed correctly.")
        # Check if username and password fields are present
        username_field = driver.find_element(By.ID, "usernameInput")
        password_field = driver.find_element(By.ID, "passwordInput")
        self.assertIsNotNone(username_field)
        self.assertIsNotNone(password_field)
        print("Username and Password fields are present.")
    def test_login_functionality(self):
        driver = self.driver
        # Perform login
        username = "johnDoe"
        password = "securePassword123"
        username_field = driver.find_element(By.ID, "usernameInput")
        password_field = driver.find_element(By.ID, "passwordInput")
        login_button = driver.find_element(By.ID, "loginButton")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the dashboard to load
        time.sleep(2)
        # Check if the user is redirected to the dashboard
        self.assertIn("Dashboard", driver.title)
        print("Successfully logged in and redirected to the Dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
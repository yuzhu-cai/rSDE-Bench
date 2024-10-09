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
        # Check if the title of the page is correct
        self.assertIn("Login", driver.title)
        print("Login page title is correct.")
        # Locate username and password fields
        username_field = driver.find_element(By.ID, "txt_username")
        password_field = driver.find_element(By.ID, "txt_password")
        login_button = driver.find_element(By.ID, "btn_login")
        # Input example data
        username = "johndoe"
        password = "password123"
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the dashboard to load
        time.sleep(2)
        # Check if we are redirected to the dashboard page
        self.assertIn("Dashboard", driver.title)
        print("Successfully logged in and redirected to the Dashboard page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
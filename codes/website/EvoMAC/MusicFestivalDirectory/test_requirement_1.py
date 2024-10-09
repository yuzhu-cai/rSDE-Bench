'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestMusicFestivalDirectory(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        # Check if the login page is accessible
        self.assertIn("Login to Music Festival Directory", driver.title)
        # Check if username and password fields are present
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login_button")
        self.assertIsNotNone(username_field)
        self.assertIsNotNone(password_field)
        self.assertIsNotNone(login_button)
        # Log in with valid credentials from users.txt
        username = "user1"  # Example username
        password = "123"    # Example password
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(2)  # Wait for the login process to complete
        # Check if redirected to the festival list page
        self.assertIn("Festival List", driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
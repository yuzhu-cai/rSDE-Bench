'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
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
    def test_login_page(self):
        driver = self.driver
        # Check if the title of the page is correct
        self.assertIn("Login to Music Festival Directory", driver.title)
        # Check if username and password fields are present
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login_button")
        self.assertIsNotNone(username_field)
        self.assertIsNotNone(password_field)
        self.assertIsNotNone(login_button)
        # Perform login with example data
        username_field.send_keys("user1")
        password_field.send_keys("123")
        login_button.click()
        # Wait for the page to load
        time.sleep(2)
        # Check if redirected to the Festival List Page
        self.assertIn("Festival List", driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
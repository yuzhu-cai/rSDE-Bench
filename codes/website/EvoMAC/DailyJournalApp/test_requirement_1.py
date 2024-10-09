'''
Test whether the website can be accessed through local port 5000.
This test checks if the login page of the Daily Journal App can be accessed.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
class TestDailyJournalApp(unittest.TestCase):
    def setUp(self):
        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        # Check if the login page is accessible
        self.assertIn("Login", driver.title)
        # Check if the username input field is present
        username_input = driver.find_element(By.ID, "username_input")
        self.assertIsNotNone(username_input)
        # Check if the password input field is present
        password_input = driver.find_element(By.ID, "password_input")
        self.assertIsNotNone(password_input)
        # Check if the login button is present
        login_button = driver.find_element(By.ID, "login_button")
        self.assertIsNotNone(login_button)
        # Check if the registration link is present
        register_link = driver.find_element(By.ID, "register_link")
        self.assertIsNotNone(register_link)
    def tearDown(self):
        # Close the WebDriver
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
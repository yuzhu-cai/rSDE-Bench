'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
class DailyJournalAppTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("Login", driver.title)
        print("Login page title is correct.")
        # Locate the username and password fields
        username_input = driver.find_element(By.ID, "username_input")
        password_input = driver.find_element(By.ID, "password_input")
        login_button = driver.find_element(By.ID, "login_button")
        # Test login with valid credentials
        username_input.send_keys("user1")
        password_input.send_keys("password123")
        login_button.click()
        # Verify that we are redirected to the Dashboard page
        self.assertIn("Dashboard", driver.title)
        print("Successfully logged in and redirected to the Dashboard page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
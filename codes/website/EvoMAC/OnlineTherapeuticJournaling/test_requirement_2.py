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
        """Test if the login page is displayed correctly."""
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        self.assertIn("User Login", driver.title)
        self.assertTrue(driver.find_element(By.ID, "login-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "username-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login-button").is_displayed())
    def test_login_correct_credentials(self):
        """Test if the user can log in with correct credentials."""
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        username_input = driver.find_element(By.ID, "username-input")
        password_input = driver.find_element(By.ID, "password-input")
        login_button = driver.find_element(By.ID, "login-button")
        username_input.send_keys("john_doe")
        password_input.send_keys("password1")
        login_button.click()
        time.sleep(2)  # Wait for the dashboard to load
        self.assertIn("User Dashboard", driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
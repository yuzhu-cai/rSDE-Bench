'''
Test whether the website can be accessed through local port 5000, specifically testing the login page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestPortfolioSiteLogin(unittest.TestCase):
    def setUp(self):
        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        # Check if the login page is accessible
        time.sleep(2)  # Wait for the page to load
        self.assertIn("User Login", driver.title)  # Check if the title is correct
        # Check if the login elements are present
        username_field = driver.find_element(By.ID, "login_username")
        password_field = driver.find_element(By.ID, "login_password")
        login_button = driver.find_element(By.ID, "login_button")
        error_message_area = driver.find_element(By.ID, "login_error_message")
        register_link = driver.find_element(By.ID, "link_register")
        # Log the presence of elements
        print("Username field found:", username_field is not None)
        print("Password field found:", password_field is not None)
        print("Login button found:", login_button is not None)
        print("Error message area found:", error_message_area is not None)
        print("Register link found:", register_link is not None)
        # Attempt to log in with valid credentials from the data storage
        username = "username1"  # Example username
        password = "password1"  # Example password
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        # Wait for the page to load after login
        time.sleep(2)
        # Check if the user is redirected to the portfolio page
        self.assertIn("User Portfolio", driver.title)
    def tearDown(self):
        # Close the WebDriver
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
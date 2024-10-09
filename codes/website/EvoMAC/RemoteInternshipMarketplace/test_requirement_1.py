'''
Test whether the website can be accessed through local port 5000 and verify the login page is accessible.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestRemoteInternshipMarketplace(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_access(self):
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        # Check if the title of the page is correct
        self.assertIn("User Login", driver.title)
        # Check if the login elements are present
        username_input = driver.find_element(By.ID, "input_username")
        password_input = driver.find_element(By.ID, "input_password")
        login_button = driver.find_element(By.ID, "btn_login")
        register_link = driver.find_element(By.ID, "link_register")
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(password_input)
        self.assertIsNotNone(login_button)
        self.assertIsNotNone(register_link)
        # Log the successful access to the login page
        print("Login page accessed successfully.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
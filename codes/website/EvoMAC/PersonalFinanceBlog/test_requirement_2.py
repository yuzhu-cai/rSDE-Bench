'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
class TestPersonalFinanceBlogLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        logging.info("Checking if the current page is the login page.")
        # Verify if the title is correct for the login page
        self.assertIn("Login", driver.title)
        logging.info("Login page title is correct.")
        # Check if the login elements are present
        self.assertIsNotNone(driver.find_element(By.ID, "username_field"))
        self.assertIsNotNone(driver.find_element(By.ID, "password_field"))
        self.assertIsNotNone(driver.find_element(By.ID, "login_button"))
        logging.info("Login elements are present on the page.")
    def test_login_functionality(self):
        driver = self.driver
        logging.info("Attempting to log in with example user data.")
        # Input username and password
        driver.find_element(By.ID, "username_field").send_keys("john_doe")
        driver.find_element(By.ID, "password_field").send_keys("abcd1234")
        driver.find_element(By.ID, "login_button").click()
        # Verify if the login was successful by checking if the dashboard is displayed
        self.assertIn("Dashboard", driver.title)
        logging.info("Login was successful, redirected to the Dashboard.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
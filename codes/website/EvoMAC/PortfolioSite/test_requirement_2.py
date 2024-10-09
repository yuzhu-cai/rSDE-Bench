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
        self.assertIn("User Login", driver.title)
        # Check if the login elements are present
        self.assertTrue(driver.find_element(By.ID, "login_username"))
        self.assertTrue(driver.find_element(By.ID, "login_password"))
        self.assertTrue(driver.find_element(By.ID, "login_button"))
        # Perform login with example data
        username = "username1"
        password = "password1"
        driver.find_element(By.ID, "login_username").send_keys(username)
        driver.find_element(By.ID, "login_password").send_keys(password)
        driver.find_element(By.ID, "login_button").click()
        # Wait for the page to load
        time.sleep(2)
        # Check if redirected to the Portfolio Page
        self.assertIn("User Portfolio", driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
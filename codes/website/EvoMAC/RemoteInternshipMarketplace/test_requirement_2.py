'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
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
    def test_login_page(self):
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        # Check if the title of the page is correct
        self.assertIn("User Login", driver.title)
        # Check if the login elements are present
        self.assertTrue(driver.find_element(By.ID, "input_username"))
        self.assertTrue(driver.find_element(By.ID, "input_password"))
        self.assertTrue(driver.find_element(By.ID, "btn_login"))
        self.assertTrue(driver.find_element(By.ID, "link_register"))
    def test_login_functionality(self):
        driver = self.driver
        time.sleep(2)  # Wait for the page to load
        # Input the username and password from example data
        username = "john_doe"
        password = "securepassword"
        driver.find_element(By.ID, "input_username").send_keys(username)
        driver.find_element(By.ID, "input_password").send_keys(password)
        driver.find_element(By.ID, "btn_login").click()
        time.sleep(2)  # Wait for the dashboard to load
        # Check if redirected to the dashboard page
        self.assertIn("Internships Dashboard", driver.title)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
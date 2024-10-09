'''
Test the elements and integrity of ALL pages in the OnlineVintageMarket application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestOnlineVintageMarket(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "johndoe"  # Example username from users.txt
        self.password = "password123"  # Example password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        # Check for the presence of the login form and its elements
        self.assertIsNotNone(driver.find_element(By.ID, "login-form"))
        self.assertIsNotNone(driver.find_element(By.ID, "username"))
        self.assertIsNotNone(driver.find_element(By.ID, "password"))
        self.assertIsNotNone(driver.find_element(By.ID, "login-button"))
    def test_home_page_elements(self):
        driver = self.driver
        # Log in to access the home page
        driver.find_element(By.ID, "username").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for the page to load
        # Check for the presence of home page elements
        self.assertIsNotNone(driver.find_element(By.ID, "header"))
        self.assertIsNotNone(driver.find_element(By.ID, "item-list"))
        self.assertIsNotNone(driver.find_element(By.ID, "create-listing-button"))
        self.assertIsNotNone(driver.find_element(By.ID, "search-field"))
        self.assertIsNotNone(driver.find_element(By.ID, "search-button"))
        self.assertIsNotNone(driver.find_element(By.ID, "search-result"))
    def test_listing_page_elements(self):
        driver = self.driver
        # Navigate to the listing page
        driver.find_element(By.ID, "create-listing-button").click()
        time.sleep(2)  # Wait for the page to load
        # Check for the presence of listing page elements
        self.assertIsNotNone(driver.find_element(By.ID, "listing-form"))
        self.assertIsNotNone(driver.find_element(By.ID, "item-name"))
        self.assertIsNotNone(driver.find_element(By.ID, "item-description"))
        self.assertIsNotNone(driver.find_element(By.ID, "item-price"))
        self.assertIsNotNone(driver.find_element(By.ID, "submit-listing-button"))
    def test_item_details_page_elements(self):
        driver = self.driver
        # Navigate back to the home page and click on an item to view details
        driver.get("http://localhost:5000")  # Go back to home page
        time.sleep(2)  # Wait for the page to load
        driver.find_element(By.ID, "item-details-button").click()  # Assuming the first item is clicked
        time.sleep(2)  # Wait for the page to load
        # Check for the presence of item details page elements
        self.assertIsNotNone(driver.find_element(By.ID, "item-title"))
        self.assertIsNotNone(driver.find_element(By.ID, "item-description"))
        self.assertIsNotNone(driver.find_element(By.ID, "item-price"))
        self.assertIsNotNone(driver.find_element(By.ID, "back-button"))
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test the elements and integrity of all pages in the ElderCareResources web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestElderCareResources(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Wait for the page to load
    def test_login_page_elements(self):
        driver = self.driver
        # Check Login Page Elements
        self.assertIsNotNone(driver.find_element(By.ID, "login-form"))
        self.assertIsNotNone(driver.find_element(By.ID, "username"))
        self.assertIsNotNone(driver.find_element(By.ID, "password"))
        self.assertIsNotNone(driver.find_element(By.ID, "login-button"))
    def test_dashboard_page_elements(self):
        driver = self.driver
        # Perform login
        driver.find_element(By.ID, "username").send_keys("john_doe")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for the dashboard to load
        # Check Dashboard Page Elements
        self.assertIsNotNone(driver.find_element(By.ID, "welcome-message"))
        self.assertIsNotNone(driver.find_element(By.ID, "resource-list"))
        self.assertIsNotNone(driver.find_element(By.ID, "contact-button"))
        self.assertIsNotNone(driver.find_element(By.ID, "logout-button"))
    def test_contact_page_elements(self):
        driver = self.driver
        # Navigate to Dashboard first
        driver.find_element(By.ID, "username").send_keys("john_doe")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for the dashboard to load
        # Navigate to Contact Page
        driver.find_element(By.ID, "contact-button").click()
        time.sleep(2)  # Wait for the contact page to load
        # Check Contact Page Elements
        self.assertIsNotNone(driver.find_element(By.ID, "contact-form"))
        self.assertIsNotNone(driver.find_element(By.ID, "contact-name"))
        self.assertIsNotNone(driver.find_element(By.ID, "contact-email"))
        self.assertIsNotNone(driver.find_element(By.ID, "contact-message"))
        self.assertIsNotNone(driver.find_element(By.ID, "submit-button"))
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
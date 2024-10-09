'''
Test cases for verifying the presence of required elements on all pages of the Online Cultural Festivals web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestCulturalFestivals(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "john_doe"  # Example username from user_data.txt
        self.password = "password123"  # Example password from user_data.txt
    def test_login_page_elements(self):
        driver = self.driver
        # Check for presence of login elements
        self.assertIsNotNone(driver.find_element(By.ID, "login-form"))
        self.assertIsNotNone(driver.find_element(By.ID, "username"))
        self.assertIsNotNone(driver.find_element(By.ID, "password"))
        self.assertIsNotNone(driver.find_element(By.ID, "login-button"))
        self.assertIsNotNone(driver.find_element(By.ID, "error-message"))
        # Perform login
        driver.find_element(By.ID, "username").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for redirection
    def test_festival_overview_page_elements(self):
        driver = self.driver
        # Check for presence of festivals overview elements
        self.assertIsNotNone(driver.find_element(By.ID, "festivals-list"))
        festivals = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'festival_item_')]")
        self.assertGreater(len(festivals), 0, "No festival items found.")
        self.assertIsNotNone(driver.find_element(By.ID, "submit-experience-button"))
        # Navigate to Festival Details Page for the first festival
        festivals[0].click()
        time.sleep(2)  # Wait for redirection
    def test_festival_details_page_elements(self):
        driver = self.driver
        # Check for presence of festival details elements
        self.assertIsNotNone(driver.find_element(By.ID, "festival-title"))
        self.assertIsNotNone(driver.find_element(By.ID, "festival-info"))
        self.assertIsNotNone(driver.find_element(By.ID, "comments-section"))
        self.assertIsNotNone(driver.find_element(By.ID, "comment-name"))
        self.assertIsNotNone(driver.find_element(By.ID, "comment-input"))
        self.assertIsNotNone(driver.find_element(By.ID, "submit-comment-button"))
        self.assertIsNotNone(driver.find_element(By.ID, "back-button"))
        # Navigate back to Festival Overview Page
        driver.find_element(By.ID, "back-button").click()
        time.sleep(2)  # Wait for redirection
    def test_user_submissions_page_elements(self):
        driver = self.driver
        # Navigate to User Submissions Page
        driver.find_element(By.ID, "submit-experience-button").click()
        time.sleep(2)  # Wait for redirection
        # Check for presence of user submissions elements
        self.assertIsNotNone(driver.find_element(By.ID, "submission-form"))
        self.assertIsNotNone(driver.find_element(By.ID, "user-name"))
        self.assertIsNotNone(driver.find_element(By.ID, "experience-description"))
        self.assertIsNotNone(driver.find_element(By.ID, "submit-button"))
        self.assertIsNotNone(driver.find_element(By.ID, "success-message"))
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
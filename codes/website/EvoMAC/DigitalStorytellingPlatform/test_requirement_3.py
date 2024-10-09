'''
Test the elements and integrity of ALL pages, ensuring that each page contains the required elements as specified in the original task requirements.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestDigitalStorytellingPlatform(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "johndoe"  # Example username from data
        self.password = "password123"  # Example password from data
    def test_login_page_elements(self):
        driver = self.driver
        self.assertIn("User Login", driver.title)
        self.assertIsNotNone(driver.find_element(By.ID, "username_field"))
        self.assertIsNotNone(driver.find_element(By.ID, "password_field"))
        self.assertIsNotNone(driver.find_element(By.ID, "login_button"))
        self.assertIsNotNone(driver.find_element(By.ID, "register_link"))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "username_field").send_keys(self.username)
        driver.find_element(By.ID, "password_field").send_keys(self.password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(1)  # Wait for redirection
        driver.get("http://localhost:5000/register")  # Navigate to registration page
        self.assertIn("User Registration", driver.title)
        self.assertIsNotNone(driver.find_element(By.ID, "reg_username_input"))
        self.assertIsNotNone(driver.find_element(By.ID, "reg_password_input"))
        self.assertIsNotNone(driver.find_element(By.ID, "reg_email_input"))
        self.assertIsNotNone(driver.find_element(By.ID, "register_button"))
    def test_story_creation_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "username_field").send_keys(self.username)
        driver.find_element(By.ID, "password_field").send_keys(self.password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(1)  # Wait for redirection
        driver.get("http://localhost:5000/create_story")  # Navigate to story creation page
        self.assertIn("Create Your Story", driver.title)
        self.assertIsNotNone(driver.find_element(By.ID, "story_title_field"))
        self.assertIsNotNone(driver.find_element(By.ID, "story_content_field"))
        self.assertIsNotNone(driver.find_element(By.ID, "save_story_button"))
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
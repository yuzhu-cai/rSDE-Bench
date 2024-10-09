'''
Test cases for EcoFriendlyLivingTips web application to ensure all required elements are present on each page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class EcoFriendlyLivingTipsTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "johndoe"  # Example username from users.txt
        self.password = "password123"  # Example password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'login-form'))
        self.assertTrue(driver.find_element(By.ID, 'username'))
        self.assertTrue(driver.find_element(By.ID, 'password'))
        self.assertTrue(driver.find_element(By.ID, 'login-button'))
        self.assertTrue(driver.find_element(By.ID, 'register-link'))
    def test_register_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'register-link').click()
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'register-form'))
        self.assertTrue(driver.find_element(By.ID, 'username'))
        self.assertTrue(driver.find_element(By.ID, 'password'))
        self.assertTrue(driver.find_element(By.ID, 'register-button'))
    def test_home_page_elements(self):
        driver = self.driver
        self.login()
        self.assertTrue(driver.find_element(By.ID, 'header'))
        self.assertTrue(driver.find_element(By.ID, 'welcome-message'))
        self.assertTrue(driver.find_element(By.ID, 'tips-link'))
        self.assertTrue(driver.find_element(By.ID, 'resources-link'))
        self.assertTrue(driver.find_element(By.ID, 'post-link'))
        self.assertTrue(driver.find_element(By.ID, 'profile-button'))
        self.assertTrue(driver.find_element(By.ID, 'contact-button'))
    def test_eco_friendly_tips_page_elements(self):
        driver = self.driver
        self.login()
        driver.find_element(By.ID, 'tips-link').click()
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'tips-list'))
        self.assertTrue(driver.find_element(By.ID, 'add-tip-form'))
        self.assertTrue(driver.find_element(By.ID, 'tip-input'))
        self.assertTrue(driver.find_element(By.ID, 'submit-tip-button'))
    def test_resources_page_elements(self):
        driver = self.driver
        self.login()
        driver.find_element(By.ID, 'resources-link').click()
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'resources-list'))
        self.assertTrue(driver.find_element(By.ID, 'resource-input'))
        self.assertTrue(driver.find_element(By.ID, 'add-resource-button'))
    def test_community_forum_page_elements(self):
        driver = self.driver
        self.login()
        driver.find_element(By.ID, 'post-link').click()
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'forum-posts'))
        self.assertTrue(driver.find_element(By.ID, 'post-input'))
        self.assertTrue(driver.find_element(By.ID, 'submit-post-button'))
    def test_profile_page_elements(self):
        driver = self.driver
        self.login()
        driver.find_element(By.ID, 'profile-button').click()
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'profile-info'))
        self.assertTrue(driver.find_element(By.ID, 'username-input'))
        self.assertTrue(driver.find_element(By.ID, 'update-profile-button'))
        self.assertTrue(driver.find_element(By.ID, 'logout-button'))
    def test_contact_page_elements(self):
        driver = self.driver
        self.login()
        driver.find_element(By.ID, 'contact-button').click()
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'contact-form'))
        self.assertTrue(driver.find_element(By.ID, 'name-input'))
        self.assertTrue(driver.find_element(By.ID, 'email-input'))
        self.assertTrue(driver.find_element(By.ID, 'message-input'))
        self.assertTrue(driver.find_element(By.ID, 'send-button'))
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, 'username').send_keys(self.username)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.ID, 'login-button').click()
        time.sleep(1)  # Wait for redirection
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
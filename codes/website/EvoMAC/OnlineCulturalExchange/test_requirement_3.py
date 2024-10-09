'''
Test the elements and integrity of ALL pages in the OnlineCulturalExchange web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class TestOnlineCulturalExchange(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "username1"  # Replace with actual username from data
        self.password = "password1"  # Replace with actual password from data
    def test_login_page_elements(self):
        """Test elements on the Login Page."""
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'login-form'))
        self.assertTrue(driver.find_element(By.ID, 'username'))
        self.assertTrue(driver.find_element(By.ID, 'password'))
        self.assertTrue(driver.find_element(By.ID, 'login-button'))
        self.assertTrue(driver.find_element(By.ID, 'error-message'))
    def test_home_page_elements(self):
        """Test elements on the Home Page."""
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'welcome-message'))
        self.assertTrue(driver.find_element(By.ID, 'culture-list'))
        self.assertTrue(driver.find_element(By.ID, 'profile-link'))
        self.assertTrue(driver.find_element(By.ID, 'contact-link'))
    def test_cultural_exchange_page_elements(self):
        """Test elements on the Cultural Exchange Page."""
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'culture-item-0').click()  # Navigate to first cultural exchange
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'exchange-form'))
        self.assertTrue(driver.find_element(By.ID, 'title'))
        self.assertTrue(driver.find_element(By.ID, 'description'))
        self.assertTrue(driver.find_element(By.ID, 'submit-exchange'))
        self.assertTrue(driver.find_element(By.ID, 'exchange-list'))
        self.assertTrue(driver.find_element(By.ID, 'home-link'))
    def test_profile_page_elements(self):
        """Test elements on the Profile Page."""
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'profile-link').click()  # Navigate to Profile Page
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'profile-header'))
        self.assertTrue(driver.find_element(By.ID, 'username-display'))
        self.assertTrue(driver.find_element(By.ID, 'logout-button'))
        self.assertTrue(driver.find_element(By.ID, 'home-link'))
    def test_contact_page_elements(self):
        """Test elements on the Contact Page."""
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'contact-link').click()  # Navigate to Contact Page
        time.sleep(1)  # Wait for page to load
        self.assertTrue(driver.find_element(By.ID, 'contact-form'))
        self.assertTrue(driver.find_element(By.ID, 'contact-name'))
        self.assertTrue(driver.find_element(By.ID, 'contact-email'))
        self.assertTrue(driver.find_element(By.ID, 'contact-message'))
        self.assertTrue(driver.find_element(By.ID, 'send-message-button'))
        self.assertTrue(driver.find_element(By.ID, 'contact-confirmation'))
        self.assertTrue(driver.find_element(By.ID, 'home-link'))
    def login(self):
        """Helper method to log in to the application."""
        driver = self.driver
        driver.find_element(By.ID, 'username').send_keys(self.username)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.ID, 'login-button').click()
        time.sleep(1)  # Wait for redirection
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
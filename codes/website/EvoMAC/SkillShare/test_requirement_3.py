'''
Test the elements and integrity of ALL pages in the SkillShare web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class SkillShareTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "johnDoe"  # Example username from data storage
        self.password = "securePassword123"  # Example password from data storage
    def login(self):
        driver = self.driver
        username_input = driver.find_element(By.ID, "usernameInput")
        password_input = driver.find_element(By.ID, "passwordInput")
        login_button = driver.find_element(By.ID, "loginButton")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.click()
        time.sleep(2)  # Wait for the page to load
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "usernameInput").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "passwordInput").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "loginButton").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "registerButton").is_displayed())
    def test_register_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "registerButton").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "usernameInput").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "passwordInput").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "registerButton").is_displayed())
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "welcomeMessage").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "featuredSkillsSection").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "viewAllSkillsButton").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "aboutButton").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "profileLink").is_displayed())
    def test_skills_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "viewAllSkillsButton").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "skillsList").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "newSkillInput").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "addSkillButton").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "removeSkillButton").is_displayed())
    def test_profile_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "profileLink").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "usernameInput").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "saveChangesButton").is_displayed())
    def test_about_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "aboutButton").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "aboutSection").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "contactInfo").is_displayed())
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
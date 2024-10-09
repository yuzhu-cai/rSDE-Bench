'''
Test the elements and integrity of ALL pages, ensuring that each page contains the required elements as specified in the original task requirements.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestGreenLivingGuide(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "user1"  # Example username from users.txt
        self.password = "password123"  # Example password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "login-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "username").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "error-message").is_displayed())
    def test_register_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "register-button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "register-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "username").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "error-message").is_displayed())
    def test_home_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "welcome-message").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "tips-section").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "articles-section").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "articles-link").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "community-link").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "explore-button").is_displayed())
    def test_tips_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "explore-button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "tips-list").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "new-tip-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "tip-title").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "tip-description").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit-tip-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "success-message").is_displayed())
    def test_articles_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "articles-link").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "articles-list").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "article-title").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "article-content").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit-article-button").is_displayed())
    def test_community_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "community-link").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "forum-posts").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "new-post-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "post-title").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "post-content").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "post-button").is_displayed())
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for the login to process
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
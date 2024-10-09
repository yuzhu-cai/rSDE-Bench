'''
Test the elements and integrity of ALL pages in ParentingAdviceForum.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestParentingAdviceForum(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "john_doe"
        self.password = "password123"
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, "username-input").send_keys(self.username)
        driver.find_element(By.ID, "password-input").send_keys(self.password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for the page to load
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "username-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register-button").is_displayed())
    def test_register_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "register-button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "username-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register-button").is_displayed())
    def test_home_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "welcome-message").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "forum-link").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "post-advice-link").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "my-account-link").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "contact-us-link").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "recent-posts").is_displayed())
    def test_forum_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "forum-link").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "thread-list").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "view-thread-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "thread-title-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "thread-content-area").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit-thread-button").is_displayed())
    def test_view_thread_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "forum-link").click()
        time.sleep(2)  # Wait for the page to load
        driver.find_element(By.ID, "view-thread-button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "view-thread-title").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "view-thread-content").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "comments-section").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "comment-input-area").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit-comment-button").is_displayed())
    def test_post_advice_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "post-advice-link").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "advice-title-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "advice-content-area").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit-advice-button").is_displayed())
    def test_my_account_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "my-account-link").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "user-info-display").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "update-profile-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "delete-account-button").is_displayed())
    def test_contact_us_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "contact-us-link").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "contact-name-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "contact-email-input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "contact-message-area").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "send-message-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "confirmation-message").is_displayed())
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
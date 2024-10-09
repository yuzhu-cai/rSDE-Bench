'''
Test the elements and integrity of all pages in the Personal Blog web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestPersonalBlog(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "john_doe"  # Example username
        self.password = "password123"  # Example password
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'username_input'))
        self.assertTrue(driver.find_element(By.ID, 'password_input'))
        self.assertTrue(driver.find_element(By.ID, 'login_button'))
        self.assertTrue(driver.find_element(By.ID, 'login_message'))
        self.assertTrue(driver.find_element(By.ID, 'register_link'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'reg_username_input'))
        self.assertTrue(driver.find_element(By.ID, 'reg_password_input'))
        self.assertTrue(driver.find_element(By.ID, 'reg_email_input'))
        self.assertTrue(driver.find_element(By.ID, 'register_button'))
        self.assertTrue(driver.find_element(By.ID, 'register_message'))
    def test_main_blog_page_elements(self):
        driver = self.driver
        self.login(driver)
        self.assertTrue(driver.find_element(By.ID, 'blog_title'))
        self.assertTrue(driver.find_element(By.ID, 'new_post_button'))
        self.assertTrue(driver.find_element(By.ID, 'view_post_button'))
        self.assertTrue(driver.find_element(By.ID, 'post_list'))
        self.assertTrue(driver.find_element(By.ID, 'logout_button'))
        self.assertTrue(driver.find_element(By.ID, 'blog_message'))
    def test_new_post_page_elements(self):
        driver = self.driver
        self.login(driver)
        driver.find_element(By.ID, 'new_post_button').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'post_title_input'))
        self.assertTrue(driver.find_element(By.ID, 'post_content_area'))
        self.assertTrue(driver.find_element(By.ID, 'submit_post_button'))
        self.assertTrue(driver.find_element(By.ID, 'post_message'))
    def test_view_post_page_elements(self):
        driver = self.driver
        self.login(driver)
        driver.find_element(By.ID, 'view_post_button').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'view_post_title'))
        self.assertTrue(driver.find_element(By.ID, 'view_post_content'))
        self.assertTrue(driver.find_element(By.ID, 'edit_post_button'))
        self.assertTrue(driver.find_element(By.ID, 'delete_post_button'))
        self.assertTrue(driver.find_element(By.ID, 'back_to_blog_button'))
    def test_edit_post_page_elements(self):
        driver = self.driver
        self.login(driver)
        driver.find_element(By.ID, 'view_post_button').click()
        time.sleep(1)  # Wait for the page to load
        driver.find_element(By.ID, 'edit_post_button').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'post_title_input'))
        self.assertTrue(driver.find_element(By.ID, 'post_content_input'))
        self.assertTrue(driver.find_element(By.ID, 'submit_post_button'))
        self.assertTrue(driver.find_element(By.ID, 'back_to_blog_button'))
    def login(self, driver):
        driver.find_element(By.ID, 'username_input').send_keys(self.username)
        driver.find_element(By.ID, 'password_input').send_keys(self.password)
        driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the page to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
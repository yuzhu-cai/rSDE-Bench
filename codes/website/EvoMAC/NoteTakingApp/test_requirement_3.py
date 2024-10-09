'''
Test the elements and integrity of all pages in NoteTakingApp.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class NoteTakingAppTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "john_doe"
        self.password = "abcd1234"
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'login_page'))
        self.assertTrue(driver.find_element(By.ID, 'username_field'))
        self.assertTrue(driver.find_element(By.ID, 'password_field'))
        self.assertTrue(driver.find_element(By.ID, 'login_button'))
        self.assertTrue(driver.find_element(By.ID, 'error_message'))
        self.assertTrue(driver.find_element(By.ID, 'register_link'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the registration page to load
        self.assertTrue(driver.find_element(By.ID, 'registration_page'))
        self.assertTrue(driver.find_element(By.ID, 'register_username_field'))
        self.assertTrue(driver.find_element(By.ID, 'register_password_field'))
        self.assertTrue(driver.find_element(By.ID, 'confirm_password_field'))
        self.assertTrue(driver.find_element(By.ID, 'register_button'))
        self.assertTrue(driver.find_element(By.ID, 'registration_success_message'))
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'dashboard_page'))
        self.assertTrue(driver.find_element(By.ID, 'notes_list'))
        self.assertTrue(driver.find_element(By.ID, 'add_note_button'))
        self.assertTrue(driver.find_element(By.ID, 'view_note_button'))
        self.assertTrue(driver.find_element(By.ID, 'search_note_button'))
        self.assertTrue(driver.find_element(By.ID, 'logout_button'))
    def test_add_note_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'add_note_button').click()
        time.sleep(1)  # Wait for the add note page to load
        self.assertTrue(driver.find_element(By.ID, 'add_note_page'))
        self.assertTrue(driver.find_element(By.ID, 'note_title_field'))
        self.assertTrue(driver.find_element(By.ID, 'note_content_field'))
        self.assertTrue(driver.find_element(By.ID, 'save_note_button'))
        self.assertTrue(driver.find_element(By.ID, 'cancel_button'))
    def test_search_note_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'search_note_button').click()
        time.sleep(1)  # Wait for the search note page to load
        self.assertTrue(driver.find_element(By.ID, 'search_note_field'))
        self.assertTrue(driver.find_element(By.ID, 'search_note_button'))
        self.assertTrue(driver.find_element(By.ID, 'search_note_result'))
        self.assertTrue(driver.find_element(By.ID, 'back_button'))
    def test_view_note_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'view_note_button').click()
        time.sleep(1)  # Wait for the view note page to load
        self.assertTrue(driver.find_element(By.ID, 'view_note_page'))
        self.assertTrue(driver.find_element(By.ID, 'note_title_filed'))
        self.assertTrue(driver.find_element(By.ID, 'note_content_filed'))
        self.assertTrue(driver.find_element(By.ID, 'edit_note_button'))
        self.assertTrue(driver.find_element(By.ID, 'delete_note_button'))
        self.assertTrue(driver.find_element(By.ID, 'back_to_dashboard_button'))
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, 'username_field').send_keys(self.username)
        driver.find_element(By.ID, 'password_field').send_keys(self.password)
        driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the dashboard to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
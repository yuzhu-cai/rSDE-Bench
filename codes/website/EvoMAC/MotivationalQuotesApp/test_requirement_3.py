'''
Test cases for MotivationalQuotesApp to ensure all required elements are present on each page.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestMotivationalQuotesApp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.login()
    def login(self):
        username = "user1"  # Example username from Users.txt
        password = "abc123"  # Example password from Users.txt
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
        time.sleep(2)  # Wait for the page to load
    def test_login_page_elements(self):
        self.driver.get("http://localhost:5000")
        self.assertTrue(self.driver.find_element(By.ID, "username_input"))
        self.assertTrue(self.driver.find_element(By.ID, "password_input"))
        self.assertTrue(self.driver.find_element(By.ID, "login_button"))
        self.assertTrue(self.driver.find_element(By.ID, "about_button"))
    def test_home_page_elements(self):
        self.driver.get("http://localhost:5000/home_page")
        self.assertTrue(self.driver.find_element(By.ID, "welcome_message"))
        self.assertTrue(self.driver.find_element(By.ID, "quotes_display"))
        self.assertTrue(self.driver.find_element(By.ID, "add_quote_button"))
        self.assertTrue(self.driver.find_element(By.ID, "favorites_button"))
    def test_add_quote_page_elements(self):
        self.driver.get("http://localhost:5000/add_quote_page")
        self.assertTrue(self.driver.find_element(By.ID, "quote_input"))
        self.assertTrue(self.driver.find_element(By.ID, "author_input"))
        self.assertTrue(self.driver.find_element(By.ID, "submit_quote_button"))
    def test_edit_quote_page_elements(self):
        self.driver.get("http://localhost:5000/edit_quote_page")
        self.assertTrue(self.driver.find_element(By.ID, "edit_quote_input"))
        self.assertTrue(self.driver.find_element(By.ID, "edit_author_input"))
        self.assertTrue(self.driver.find_element(By.ID, "update_quote_button"))
    def test_delete_confirmation_page_elements(self):
        self.driver.get("http://localhost:5000/delete_confirmation_page")
        self.assertTrue(self.driver.find_element(By.ID, "confirm_message"))
        self.assertTrue(self.driver.find_element(By.ID, "confirm_deletion_button"))
        self.assertTrue(self.driver.find_element(By.ID, "cancel_button"))
    def test_favorites_page_elements(self):
        self.driver.get("http://localhost:5000/favorites_page")
        self.assertTrue(self.driver.find_element(By.ID, "favorites_display"))
    def test_about_page_elements(self):
        self.driver.get("http://localhost:5000/about_page")
        self.assertTrue(self.driver.find_element(By.ID, "app_description"))
        self.assertTrue(self.driver.find_element(By.ID, "developer_info"))
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
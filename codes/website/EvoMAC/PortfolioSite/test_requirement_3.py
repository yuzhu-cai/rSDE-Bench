'''
Test the elements and integrity of all pages in the PortfolioSite web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestPortfolioSite(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "username1"  # Example username from users.txt
        self.password = "password1"  # Example password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        # Check for Login Page elements
        self.assertIsNotNone(driver.find_element(By.ID, "login_username"))
        self.assertIsNotNone(driver.find_element(By.ID, "login_password"))
        self.assertIsNotNone(driver.find_element(By.ID, "login_button"))
        self.assertIsNotNone(driver.find_element(By.ID, "login_error_message"))
        self.assertIsNotNone(driver.find_element(By.ID, "link_register"))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "login_username").send_keys(self.username)
        driver.find_element(By.ID, "login_password").send_keys(self.password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(1)  # Wait for the page to load
        # Navigate to Registration Page
        driver.get("http://localhost:5000/register")
        self.assertIsNotNone(driver.find_element(By.ID, "reg_email"))
        self.assertIsNotNone(driver.find_element(By.ID, "reg_username"))
        self.assertIsNotNone(driver.find_element(By.ID, "reg_password"))
        self.assertIsNotNone(driver.find_element(By.ID, "reg_button"))
    def test_portfolio_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "login_username").send_keys(self.username)
        driver.find_element(By.ID, "login_password").send_keys(self.password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(1)  # Wait for the page to load
        # Check for Portfolio Page elements
        self.assertIsNotNone(driver.find_element(By.ID, "project_list"))
        self.assertIsNotNone(driver.find_element(By.ID, "new_project_link"))
        self.assertIsNotNone(driver.find_element(By.ID, "new_project_description"))
        self.assertIsNotNone(driver.find_element(By.ID, "add_project_button"))
        self.assertIsNotNone(driver.find_element(By.ID, "delete_project_button"))
        self.assertIsNotNone(driver.find_element(By.ID, "blog_button"))
        self.assertIsNotNone(driver.find_element(By.ID, "contact_button"))
    def test_blog_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "login_username").send_keys(self.username)
        driver.find_element(By.ID, "login_password").send_keys(self.password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(1)  # Wait for the page to load
        # Navigate to Blog Page
        driver.find_element(By.ID, "blog_button").click()
        time.sleep(1)  # Wait for the page to load
        # Check for Blog Page elements
        self.assertIsNotNone(driver.find_element(By.ID, "blog_posts"))
        self.assertIsNotNone(driver.find_element(By.ID, "blog_title"))
        self.assertIsNotNone(driver.find_element(By.ID, "blog_content"))
        self.assertIsNotNone(driver.find_element(By.ID, "publish_blog_button"))
        self.assertIsNotNone(driver.find_element(By.ID, "delete_blog_button"))
    def test_contact_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "login_username").send_keys(self.username)
        driver.find_element(By.ID, "login_password").send_keys(self.password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(1)  # Wait for the page to load
        # Navigate to Contact Page
        driver.find_element(By.ID, "contact_button").click()
        time.sleep(1)  # Wait for the page to load
        # Check for Contact Page elements
        self.assertIsNotNone(driver.find_element(By.ID, "contact_name"))
        self.assertIsNotNone(driver.find_element(By.ID, "contact_email"))
        self.assertIsNotNone(driver.find_element(By.ID, "contact_message"))
        self.assertIsNotNone(driver.find_element(By.ID, "send_message_button"))
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
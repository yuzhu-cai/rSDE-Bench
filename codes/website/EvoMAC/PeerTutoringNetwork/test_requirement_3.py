'''
Test the elements and integrity of all pages in the PeerTutoringNetwork web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestPeerTutoringNetwork(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "johndoe"  # Example username from data
        self.password = "password123"  # Example password from data
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'txt_username'))
        self.assertTrue(driver.find_element(By.ID, 'txt_password'))
        self.assertTrue(driver.find_element(By.ID, 'btn_login'))
        self.assertTrue(driver.find_element(By.ID, 'link_register'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'link_register').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'txt_new_username'))
        self.assertTrue(driver.find_element(By.ID, 'txt_new_password'))
        self.assertTrue(driver.find_element(By.ID, 'txt_email'))
        self.assertTrue(driver.find_element(By.ID, 'btn_register'))
        self.assertTrue(driver.find_element(By.ID, 'link_login'))
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'btn_view_tutors'))
        self.assertTrue(driver.find_element(By.ID, 'btn_request_tutoring'))
        self.assertTrue(driver.find_element(By.ID, 'link_logout'))
        self.assertTrue(driver.find_element(By.ID, 'link_profile'))
        self.assertTrue(driver.find_element(By.ID, 'link_contact_us'))
    def test_tutors_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'btn_view_tutors').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'div_tutor_list'))
    def test_request_tutoring_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'btn_request_tutoring').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'txt_subject'))
        self.assertTrue(driver.find_element(By.ID, 'txt_details'))
        self.assertTrue(driver.find_element(By.ID, 'txt_date'))
        self.assertTrue(driver.find_element(By.ID, 'btn_submit_request'))
        self.assertTrue(driver.find_element(By.ID, 'link_cancel'))
    def test_profile_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'link_profile').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'txt_username_display'))
        self.assertTrue(driver.find_element(By.ID, 'txt_email_display'))
        self.assertTrue(driver.find_element(By.ID, 'link_logout'))
    def test_contact_us_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'link_contact_us').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'txt_contact_name'))
        self.assertTrue(driver.find_element(By.ID, 'txt_contact_email'))
        self.assertTrue(driver.find_element(By.ID, 'txt_contact_message'))
        self.assertTrue(driver.find_element(By.ID, 'btn_send'))
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, 'txt_username').send_keys(self.username)
        driver.find_element(By.ID, 'txt_password').send_keys(self.password)
        driver.find_element(By.ID, 'btn_login').click()
        time.sleep(1)  # Wait for the dashboard to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
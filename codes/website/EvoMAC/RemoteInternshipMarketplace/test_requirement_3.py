'''
Test the elements and integrity of ALL pages in the RemoteInternshipMarketplace web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestRemoteInternshipMarketplace(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "john_doe"  # Example username from users.txt
        self.password = "securepassword"  # Example password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'input_username'))
        self.assertTrue(driver.find_element(By.ID, 'input_password'))
        self.assertTrue(driver.find_element(By.ID, 'btn_login'))
        self.assertTrue(driver.find_element(By.ID, 'link_register'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'link_register').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'input_username'))
        self.assertTrue(driver.find_element(By.ID, 'input_first_name'))
        self.assertTrue(driver.find_element(By.ID, 'input_last_name'))
        self.assertTrue(driver.find_element(By.ID, 'input_email'))
        self.assertTrue(driver.find_element(By.ID, 'input_password'))
        self.assertTrue(driver.find_element(By.ID, 'input_confirm_password'))
        self.assertTrue(driver.find_element(By.ID, 'btn_register'))
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'heading_welcome'))
        self.assertTrue(driver.find_element(By.ID, 'btn_view_internships'))
        self.assertTrue(driver.find_element(By.ID, 'btn_post_internship'))
        self.assertTrue(driver.find_element(By.ID, 'list_internships'))
        self.assertTrue(driver.find_element(By.ID, 'btn_logout'))
    def test_internship_listings_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'btn_view_internships').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'input_search'))
        self.assertTrue(driver.find_element(By.ID, 'btn_search_intership'))
        self.assertTrue(driver.find_element(By.ID, 'list_results'))
        self.assertTrue(driver.find_element(By.ID, 'list_available_internships'))
        # Assuming there's at least one internship to check for view details button
        self.assertTrue(driver.find_element(By.ID, 'btn_view_details_1'))
    def test_post_internship_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'btn_post_internship').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'input_internship_title'))
        self.assertTrue(driver.find_element(By.ID, 'input_internship_desc'))
        self.assertTrue(driver.find_element(By.ID, 'input_internship_category'))
        self.assertTrue(driver.find_element(By.ID, 'input_application_deadline'))
        self.assertTrue(driver.find_element(By.ID, 'btn_submit_internship'))
    def test_internship_details_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'btn_view_internships').click()
        time.sleep(1)  # Wait for the page to load
        driver.find_element(By.ID, 'btn_view_details_1').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'heading_internship_title'))
        self.assertTrue(driver.find_element(By.ID, 'para_internship_desc'))
        self.assertTrue(driver.find_element(By.ID, 'para_internship_cate'))
        self.assertTrue(driver.find_element(By.ID, 'para_internship_ddl'))
        self.assertTrue(driver.find_element(By.ID, 'btn_apply_now'))
        self.assertTrue(driver.find_element(By.ID, 'btn_back_to_listings'))
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, 'input_username').send_keys(self.username)
        driver.find_element(By.ID, 'input_password').send_keys(self.password)
        driver.find_element(By.ID, 'btn_login').click()
        time.sleep(1)  # Wait for the dashboard to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
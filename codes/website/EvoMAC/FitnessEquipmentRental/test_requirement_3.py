'''
Test the elements and integrity of all pages in the FitnessEquipmentRental application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestFitnessEquipmentRental(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.login()
    def login(self):
        driver = self.driver
        username = "john_doe"  # Example username from data
        password = "password123"  # Example password from data
        driver.find_element(By.ID, "username_field").send_keys(username)
        driver.find_element(By.ID, "password_field").send_keys(password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(2)  # Wait for the page to load
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "login_form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "username_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register_link").is_displayed())
    def test_register_page_elements(self):
        driver = self.driver
        driver.get("http://localhost:5000/register")
        self.assertTrue(driver.find_element(By.ID, "register_form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "username_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "name_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "email_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register_button").is_displayed())
    def test_homepage_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "welcome_message").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "equipment_listing").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "promotions_section").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "browse_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "my_rental_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "help_button").is_displayed())
    def test_equipment_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "browse_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "equipment_listing").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "show_details_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "equipment_details").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "rent_button").is_displayed())
    def test_rental_form_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "rent_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "rental_form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "equipment_id_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "rental_duration_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "user_details_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit_rental_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "rental_confirmation_msg").is_displayed())
    def test_my_rentals_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "my_rental_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "my_current_rentals_listing").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "return_equipment_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "my_past_rentals_listing").is_displayed())
    def test_return_equipment_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "return_equipment_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "return_form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "rental_id_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "confirm_return_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "return_confirmation_msg").is_displayed())
    def test_help_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "help_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "faq_section").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "accessibility_info").is_displayed())
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
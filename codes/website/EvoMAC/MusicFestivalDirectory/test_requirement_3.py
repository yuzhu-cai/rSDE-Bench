'''
Test the elements and integrity of ALL pages in the Music Festival Directory web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class MusicFestivalDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "user1"  # Example username from users.txt
        self.password = "123"     # Example password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        # Check for presence of login elements
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login_button")
        error_message_display = driver.find_element(By.ID, "error_message")
        self.assertIsNotNone(username_field, "Username field is missing")
        self.assertIsNotNone(password_field, "Password field is missing")
        self.assertIsNotNone(login_button, "Login button is missing")
        self.assertIsNotNone(error_message_display, "Error message display is missing")
    def test_festival_list_page_elements(self):
        driver = self.driver
        self.login()
        time.sleep(1)  # Wait for page to load
        # Check for presence of festival list elements
        festival_list_container = driver.find_element(By.ID, "festival_list")
        add_festival_button = driver.find_element(By.ID, "add_festival_page_button")
        self.assertIsNotNone(festival_list_container, "Festival list container is missing")
        self.assertIsNotNone(add_festival_button, "Add new festival button is missing")
    def test_festival_details_page_elements(self):
        driver = self.driver
        self.login()
        time.sleep(1)  # Wait for page to load
        driver.find_element(By.ID, "festival_item_0").click()  # Click on the first festival item
        time.sleep(1)  # Wait for page to load
        # Check for presence of festival details elements
        festival_name_display = driver.find_element(By.ID, "festival_name")
        location_display = driver.find_element(By.ID, "festival_location")
        date_display = driver.find_element(By.ID, "festival_date")
        lineup_display = driver.find_element(By.ID, "festival_lineup")
        back_to_list_button = driver.find_element(By.ID, "back_to_list_button")
        self.assertIsNotNone(festival_name_display, "Festival name display is missing")
        self.assertIsNotNone(location_display, "Location display is missing")
        self.assertIsNotNone(date_display, "Date display is missing")
        self.assertIsNotNone(lineup_display, "Lineup display is missing")
        self.assertIsNotNone(back_to_list_button, "Back to list button is missing")
    def test_add_festival_page_elements(self):
        driver = self.driver
        self.login()
        time.sleep(1)  # Wait for page to load
        driver.find_element(By.ID, "add_festival_page_button").click()  # Click to add new festival
        time.sleep(1)  # Wait for page to load
        # Check for presence of add festival elements
        festival_name_input = driver.find_element(By.ID, "add_festival_name")
        location_input = driver.find_element(By.ID, "add_festival_location")
        date_input = driver.find_element(By.ID, "add_festival_date")
        lineup_input = driver.find_element(By.ID, "add_festival_lineup")
        submit_button = driver.find_element(By.ID, "submit_button")
        admin_message_display = driver.find_element(By.ID, "admin_message")
        self.assertIsNotNone(festival_name_input, "Festival name input is missing")
        self.assertIsNotNone(location_input, "Location input is missing")
        self.assertIsNotNone(date_input, "Date input is missing")
        self.assertIsNotNone(lineup_input, "Lineup input is missing")
        self.assertIsNotNone(submit_button, "Submit button is missing")
        self.assertIsNotNone(admin_message_display, "Success/Error message display is missing")
    def login(self):
        driver = self.driver
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login_button")
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        login_button.click()
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
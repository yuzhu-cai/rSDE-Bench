'''
Test the elements and integrity of ALL pages in the FitnessTracker web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
class FitnessTrackerTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def login(self, username, password):
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "username_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "error_message").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register_link").is_displayed())
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "register_link").click()
        self.assertTrue(driver.find_element(By.ID, "register_username_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register_password_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "confirm_password_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "current_weight_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "goal_weight_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "registration_success_message").is_displayed())
    def test_dashboard_page_elements(self):
        self.login("john_doe", "abcd1234")  # Use valid credentials
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "goal_weight").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "current_weight").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "update_goal_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "log_activity_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "view_activity_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "logout_button").is_displayed())
    def test_update_goal_page_elements(self):
        self.login("john_doe", "abcd1234")
        self.driver.find_element(By.ID, "update_goal_button").click()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "goal_value_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "save_goal_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "cancel_button").is_displayed())
    def test_log_activity_page_elements(self):
        self.login("john_doe", "abcd1234")
        self.driver.find_element(By.ID, "log_activity_button").click()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "activity_type_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "calories_burned_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "current_weight_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "save_activity_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "cancel_button").is_displayed())
    def test_view_activity_page_elements(self):
        self.login("john_doe", "abcd1234")
        self.driver.find_element(By.ID, "view_activity_button").click()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "activity_log_list").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "activity_type_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "edit_activity_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "delete_activity_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "back_to_dashboard_button").is_displayed())
    def test_edit_activity_page_elements(self):
        self.login("john_doe", "abcd1234")
        self.driver.find_element(By.ID, "view_activity_button").click()
        self.driver.find_element(By.ID, "activity_type_field").send_keys("Running")  # Example activity
        self.driver.find_element(By.ID, "edit_activity_button").click()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "activity_type_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "calories_burned_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "current_weight_field").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "save_activity_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "cancel_button").is_displayed())
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
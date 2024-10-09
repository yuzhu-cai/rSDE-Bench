'''
Test the elements and integrity of all pages in the RecipeHub application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class RecipeHubTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "user1"  # Example username from users.txt
        self.password = "password123"  # Example password from users.txt
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, "username_input").send_keys(self.username)
        driver.find_element(By.ID, "password_input").send_keys(self.password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(2)  # Wait for the page to load
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "username_input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password_input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "error_message").is_displayed())
    def test_home_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "welcome_message").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "view_recipes_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit_recipe_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "profile_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "logout_button").is_displayed())
    def test_recipe_submission_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "submit_recipe_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "recipe_title_input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "ingredients_input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "instructions_input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit_recipe_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submission_success_message").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submission_error_message").is_displayed())
    def test_recipe_browsing_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "view_recipes_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "search_input").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "search_button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "search_result").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "recipe_list").is_displayed())
        # Check for recipe details buttons (assuming at least one recipe exists)
        self.assertTrue(driver.find_element(By.ID, "recipe_details_button_0").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "back_to_home_button").is_displayed())
    def test_user_profile_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "profile_button").click()
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "username_display").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "user_recipes_list").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "delete_account_button").is_displayed())
    def test_recipe_details_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "view_recipes_button").click()
        time.sleep(2)  # Wait for the page to load
        driver.find_element(By.ID, "recipe_details_button_0").click()  # Accessing the first recipe details
        time.sleep(2)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, "recipe_title").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "recipe_ingredient").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "recipe_instruction").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "back_to_home_button").is_displayed())
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
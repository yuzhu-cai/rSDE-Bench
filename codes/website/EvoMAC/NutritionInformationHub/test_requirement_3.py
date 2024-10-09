'''
Test the elements and integrity of all pages in the Nutrition Information Hub application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestNutritionInformationHub(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "username1"  # Use the first username from users.txt
        self.password = "password1"  # Use the corresponding password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        # Check for login page elements
        self.assertIsNotNone(driver.find_element(By.ID, 'usernameField'), "usernameField not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'passwordField'), "passwordField not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'loginButton'), "loginButton not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'errorMessage'), "errorMessage not found")
    def test_home_page_elements(self):
        driver = self.driver
        self.login(driver)
        time.sleep(1)  # Wait for the page to load
        # Check for home page elements
        self.assertIsNotNone(driver.find_element(By.ID, 'nutritionInfoLink'), "nutritionInfoLink not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'recipeTrackerLink'), "recipeTrackerLink not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'logoutButton'), "logoutButton not found")
    def test_nutrition_information_page_elements(self):
        driver = self.driver
        self.login(driver)
        time.sleep(1)  # Wait for the page to load
        driver.find_element(By.ID, 'nutritionInfoLink').click()
        time.sleep(1)  # Wait for the page to load
        # Check for nutrition information page elements
        self.assertIsNotNone(driver.find_element(By.ID, 'nutritionInfoTitle'), "nutritionInfoTitle not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'searchField'), "searchField not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'searchButton'), "searchButton not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'foodList'), "foodList not found")
    def test_recipe_tracker_page_elements(self):
        driver = self.driver
        self.login(driver)
        time.sleep(1)  # Wait for the page to load
        driver.find_element(By.ID, 'recipeTrackerLink').click()
        time.sleep(1)  # Wait for the page to load
        # Check for recipe tracker page elements
        self.assertIsNotNone(driver.find_element(By.ID, 'recipeTrackerTitle'), "recipeTrackerTitle not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'recipeNameField'), "recipeNameField not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'ingredientsField'), "ingredientsField not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'instructionsField'), "instructionsField not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'saveRecipeButton'), "saveRecipeButton not found")
        self.assertIsNotNone(driver.find_element(By.ID, 'savedRecipesList'), "savedRecipesList not found")
    def login(self, driver):
        # Perform login
        username_field = driver.find_element(By.ID, 'usernameField')
        password_field = driver.find_element(By.ID, 'passwordField')
        login_button = driver.find_element(By.ID, 'loginButton')
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        login_button.click()
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
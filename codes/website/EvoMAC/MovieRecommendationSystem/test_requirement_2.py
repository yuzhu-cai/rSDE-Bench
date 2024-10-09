'''
Test whether the first page of the website is the login page and whether it can log in correctly based on the example data provided in the Task.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
class TestMovieRecommendationSystem(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page(self):
        driver = self.driver
        # Check if the current page is the login page
        self.assertIn("User Login", driver.title)
        print("Login page title verified.")
        # Locate the username and password fields
        username_field = driver.find_element(By.ID, "usernameField")
        password_field = driver.find_element(By.ID, "passwordField")
        login_button = driver.find_element(By.ID, "loginButton")
        # Input the example username and password
        username_field.send_keys("user1")
        password_field.send_keys("secret123")
        login_button.click()
        # Verify if redirected to the home page
        self.assertIn("Movie Recommendations", driver.title)
        print("Successfully logged in and redirected to the home page.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test whether the website can be accessed through local port 5000 and verify the login page is accessible.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestDigitalArtworkGallery(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
    def test_login_page_accessibility(self):
        driver = self.driver
        # Wait for the page to load
        time.sleep(2)
        # Check if the login page is accessible by verifying the presence of the username field
        try:
            username_field = driver.find_element(By.ID, "username_field")
            self.assertTrue(username_field.is_displayed(), "Login page is not accessible: Username field not found.")
            print("Login page is accessible: Username field found.")
        except Exception as e:
            self.fail(f"Login page is not accessible: {str(e)}")
    def tearDown(self):
        # Close the browser after the test
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
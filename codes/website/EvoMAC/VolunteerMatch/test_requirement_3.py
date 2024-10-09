'''
Test the elements and integrity of all pages in the VolunteerMatch web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class VolunteerMatchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Allow time for the page to load
    def test_login_page_elements(self):
        driver = self.driver
        # Verify the presence of the login form
        self.assertIsNotNone(driver.find_element(By.ID, 'login-form'))
        # Verify the presence of the username field
        self.assertIsNotNone(driver.find_element(By.ID, 'username'))
        # Verify the presence of the password field
        self.assertIsNotNone(driver.find_element(By.ID, 'password'))
        # Verify the presence of the login button
        self.assertIsNotNone(driver.find_element(By.ID, 'login-button'))
    def test_volunteer_dashboard_elements(self):
        driver = self.driver
        # Login to access the dashboard
        self.login("username1", "password1")  # Use valid credentials from data storage
        time.sleep(2)  # Allow time for the dashboard to load
        # Verify the presence of the dashboard header
        self.assertIsNotNone(driver.find_element(By.ID, 'dashboard-header'))
        # Verify the presence of the available opportunities section
        self.assertIsNotNone(driver.find_element(By.ID, 'available-opportunities'))
        # Verify the presence of opportunity items
        opportunities = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'opportunity-')]")
        self.assertGreater(len(opportunities), 0, "No opportunities found.")
        # Verify the presence of apply buttons
        apply_buttons = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'apply-button-')]")
        self.assertGreater(len(apply_buttons), 0, "No apply buttons found.")
        # Verify the presence of the logout button
        self.assertIsNotNone(driver.find_element(By.ID, 'logout-button'))
    def test_opportunity_details_page_elements(self):
        driver = self.driver
        # Login to access the dashboard
        self.login("username1", "password1")  # Use valid credentials from data storage
        time.sleep(2)  # Allow time for the dashboard to load
        # Click on the first apply button to navigate to the opportunity details page
        apply_button = driver.find_element(By.XPATH, "//*[starts-with(@id, 'apply-button-')][1]")
        apply_button.click()
        time.sleep(2)  # Allow time for the opportunity details page to load
        # Verify the presence of the opportunity details header
        self.assertIsNotNone(driver.find_element(By.ID, 'opp-details-header'))
        # Verify the presence of the description section
        self.assertIsNotNone(driver.find_element(By.ID, 'opp-description'))
        # Verify the presence of the apply form
        self.assertIsNotNone(driver.find_element(By.ID, 'apply-form'))
        # Verify the presence of the name field
        self.assertIsNotNone(driver.find_element(By.ID, 'applicant-name'))
        # Verify the presence of the email field
        self.assertIsNotNone(driver.find_element(By.ID, 'applicant-email'))
        # Verify the presence of the submit application button
        self.assertIsNotNone(driver.find_element(By.ID, 'submit-application'))
    def login(self, username, password):
        driver = self.driver
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'login-button').click()
        time.sleep(2)  # Allow time for the login process
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
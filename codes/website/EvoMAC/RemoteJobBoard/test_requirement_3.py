'''
Test the elements and integrity of all pages in the RemoteJobBoard application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestRemoteJobBoard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        time.sleep(2)  # Wait for the page to load
    def test_login_page_elements(self):
        driver = self.driver
        # Check for Login Page elements
        username_input = driver.find_element(By.ID, "username-input")
        password_input = driver.find_element(By.ID, "password-input")
        login_button = driver.find_element(By.ID, "login-button")
        register_button = driver.find_element(By.ID, "register-button")
        error_message = driver.find_element(By.ID, "error-message")
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(password_input)
        self.assertIsNotNone(login_button)
        self.assertIsNotNone(register_button)
        self.assertIsNotNone(error_message)
    def test_register_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "register-button").click()
        time.sleep(2)  # Wait for the page to load
        # Check for Register Page elements
        username_input = driver.find_element(By.ID, "username-input")
        password_input = driver.find_element(By.ID, "password-input")
        register_button = driver.find_element(By.ID, "register-button")
        error_message = driver.find_element(By.ID, "error-message")
        self.assertIsNotNone(username_input)
        self.assertIsNotNone(password_input)
        self.assertIsNotNone(register_button)
        self.assertIsNotNone(error_message)
    def test_home_page_elements(self):
        self.login()
        driver = self.driver
        # Check for Home Page elements
        main_content = driver.find_element(By.ID, "main-content")
        browse_jobs_button = driver.find_element(By.ID, "browse-jobs-button")
        post_job_button = driver.find_element(By.ID, "post-job-button")
        edit_profile_button = driver.find_element(By.ID, "edit-profile-button")
        login_link = driver.find_element(By.ID, "login-link")
        self.assertIsNotNone(main_content)
        self.assertIsNotNone(browse_jobs_button)
        self.assertIsNotNone(post_job_button)
        self.assertIsNotNone(edit_profile_button)
        self.assertIsNotNone(login_link)
    def test_job_listings_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "browse-jobs-button").click()
        time.sleep(2)  # Wait for the page to load
        # Check for Job Listings Page elements
        job_list_container = driver.find_element(By.ID, "job-list-container")
        job_postings = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'job-posting-')]")
        apply_buttons = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'apply-button-')]")
        self.assertIsNotNone(job_list_container)
        self.assertGreater(len(job_postings), 0)
        self.assertGreater(len(apply_buttons), 0)
    def test_post_job_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "post-job-button").click()
        time.sleep(2)  # Wait for the page to load
        # Check for Post Job Page elements
        job_title_input = driver.find_element(By.ID, "job-title-input")
        company_name_input = driver.find_element(By.ID, "company-name-input")
        job_description_textarea = driver.find_element(By.ID, "job-description-textarea")
        submit_button = driver.find_element(By.ID, "submit-job-button")
        self.assertIsNotNone(job_title_input)
        self.assertIsNotNone(company_name_input)
        self.assertIsNotNone(job_description_textarea)
        self.assertIsNotNone(submit_button)
    def test_user_profile_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "edit-profile-button").click()
        time.sleep(2)  # Wait for the page to load
        # Check for User Profile Page elements
        username_display = driver.find_element(By.ID, "username-display")
        email_display = driver.find_element(By.ID, "email-display")
        edit_profile_button = driver.find_element(By.ID, "edit-profile-button")
        job_list = driver.find_element(By.ID, "job-list")
        logout_button = driver.find_element(By.ID, "logout-button")
        self.assertIsNotNone(username_display)
        self.assertIsNotNone(email_display)
        self.assertIsNotNone(edit_profile_button)
        self.assertIsNotNone(job_list)
        self.assertIsNotNone(logout_button)
    def login(self):
        driver = self.driver
        username = "john_doe"  # Use a valid username from users.txt
        password = "password123"  # Use a valid password from users.txt
        driver.find_element(By.ID, "username-input").send_keys(username)
        driver.find_element(By.ID, "password-input").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for the login to process
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
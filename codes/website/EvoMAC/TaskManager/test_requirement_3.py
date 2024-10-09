'''
Test the elements and integrity of ALL pages in the Task_Manager web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TaskManagerTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "johndoe"  # Example username from user data
        self.password = "password123"  # Example password from user data
    def test_login_page_elements(self):
        driver = self.driver
        # Check Login Page Elements
        self.assertTrue(driver.find_element(By.ID, 'username_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'password_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'login_button').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'register_link').is_displayed())
    def test_registration_page_elements(self):
        driver = self.driver
        # Navigate to Registration Page
        driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the page to load
        # Check Registration Page Elements
        self.assertTrue(driver.find_element(By.ID, 'reg_username_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'reg_password_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'reg_email_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'register_button').is_displayed())
    def test_home_page_elements(self):
        driver = self.driver
        # Log in to access Home Page
        driver.find_element(By.ID, 'username_input').send_keys(self.username)
        driver.find_element(By.ID, 'password_input').send_keys(self.password)
        driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the page to load
        # Check Home Page Elements
        self.assertTrue(driver.find_element(By.ID, 'task_list').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'add_task_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'due_date_input').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'add_task_button').is_displayed())
        # Check Remove Task Button for each task (assuming there are tasks)
        # This part may need to be adjusted based on the actual number of tasks
        tasks = driver.find_elements(By.CSS_SELECTOR, '[id^="remove_task_button_"]')
        for task in tasks:
            self.assertTrue(task.is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'back_to_login_button').is_displayed())
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
'''
Test the elements and integrity of ALL pages in the TravelDiary web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TravelDiaryTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.driver.implicitly_wait(10)
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'inputUsername').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'inputPassword').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnLogin').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'linkRegister').is_displayed())
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'linkRegister').click()
        time.sleep(1)
        self.assertTrue(driver.find_element(By.ID, 'inputUsername').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'inputPassword').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'inputEmail').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnRegister').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'linkLogin').is_displayed())
    def test_home_page_elements(self):
        driver = self.driver
        self.login("john_doe", "password1")  # Using existing user credentials
        self.assertTrue(driver.find_element(By.ID, 'headerTitle').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnViewDiary').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnAddEntry').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnAbout').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'listEntries').is_displayed())
    def test_diary_entry_page_elements(self):
        driver = self.driver
        self.login("john_doe", "password1")
        driver.find_element(By.ID, 'btnAddEntry').click()
        time.sleep(1)
        self.assertTrue(driver.find_element(By.ID, 'inputEntryTitle').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'textareaEntry').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnSaveEntry').is_displayed())
    def test_view_diary_page_elements(self):
        driver = self.driver
        self.login("john_doe", "password1")
        driver.find_element(By.ID, 'btnViewDiary').click()
        time.sleep(1)
        self.assertTrue(driver.find_element(By.ID, 'listDiaryEntries').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnEdit').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnDelete').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnReturn').is_displayed())
    def test_edit_diary_page_elements(self):
        driver = self.driver
        self.login("john_doe", "password1")
        driver.find_element(By.ID, 'btnViewDiary').click()
        time.sleep(1)
        driver.find_element(By.ID, 'btnEdit').click()
        time.sleep(1)
        self.assertTrue(driver.find_element(By.ID, 'inputEntryTitle').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'textareaEntry').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'btnUpdateEntry').is_displayed())
    def test_about_page_elements(self):
        driver = self.driver
        self.login("john_doe", "password1")
        driver.find_element(By.ID, 'btnAbout').click()
        time.sleep(1)
        self.assertTrue(driver.find_element(By.ID, 'headerTitle').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'contentInfo').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'linkContact').is_displayed())
    def login(self, username, password):
        driver = self.driver
        driver.find_element(By.ID, 'inputUsername').send_keys(username)
        driver.find_element(By.ID, 'inputPassword').send_keys(password)
        driver.find_element(By.ID, 'btnLogin').click()
        time.sleep(1)
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
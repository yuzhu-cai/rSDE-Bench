'''
Test the elements and integrity of ALL pages in the VirtualBookPublishing web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestVirtualBookPublishing(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "username1"  # Example username from data
        self.password = "password1"  # Example password from data
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'username'))
        self.assertTrue(driver.find_element(By.ID, 'password'))
        self.assertTrue(driver.find_element(By.ID, 'loginBtn'))
        self.assertTrue(driver.find_element(By.ID, 'registrationLink'))
        self.assertTrue(driver.find_element(By.ID, 'aboutLink'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'registrationLink').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'regUsername'))
        self.assertTrue(driver.find_element(By.ID, 'regPassword'))
        self.assertTrue(driver.find_element(By.ID, 'regSubmit'))
        self.assertTrue(driver.find_element(By.ID, 'loginLink'))
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'welcomeMsg'))
        self.assertTrue(driver.find_element(By.ID, 'createBookBtn'))
        self.assertTrue(driver.find_element(By.ID, 'viewBooksBtn'))
    def test_create_new_book_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'createBookBtn').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'bookTitle'))
        self.assertTrue(driver.find_element(By.ID, 'bookAuthor'))
        self.assertTrue(driver.find_element(By.ID, 'bookContent'))
        self.assertTrue(driver.find_element(By.ID, 'submitBook'))
        self.assertTrue(driver.find_element(By.ID, 'cancelCreate'))
    def test_view_my_books_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'viewBooksBtn').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'booksList'))
        # Check for at least one view button for each book
        books = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'viewBook_')]")
        self.assertGreater(len(books), 0)
    def test_view_book_details_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'viewBooksBtn').click()
        time.sleep(1)  # Wait for the page to load
        first_book_view_button = driver.find_element(By.XPATH, "//*[starts-with(@id, 'viewBook_')][1]")
        first_book_view_button.click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'detailTitle'))
        self.assertTrue(driver.find_element(By.ID, 'detailAuthor'))
        self.assertTrue(driver.find_element(By.ID, 'detailContent'))
        self.assertTrue(driver.find_element(By.ID, 'backToMyBooks'))
    def test_about_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'aboutLink').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'appDescription'))
        self.assertTrue(driver.find_element(By.ID, 'versionInfo'))
        self.assertTrue(driver.find_element(By.ID, 'contactInfo'))
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, 'username').send_keys(self.username)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.ID, 'loginBtn').click()
        time.sleep(1)  # Wait for the page to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
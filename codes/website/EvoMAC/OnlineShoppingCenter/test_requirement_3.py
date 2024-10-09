'''
Test the elements and integrity of all pages in the online shopping center web application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestOnlineShoppingCenter(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "johndoe"  # Example username from users.txt
        self.password = "secret123"  # Example password from users.txt
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'username_input'))
        self.assertTrue(driver.find_element(By.ID, 'password_input'))
        self.assertTrue(driver.find_element(By.ID, 'login_button'))
        self.assertTrue(driver.find_element(By.ID, 'register_link'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'reg_username_input'))
        self.assertTrue(driver.find_element(By.ID, 'reg_password_input'))
        self.assertTrue(driver.find_element(By.ID, 'reg_email_input'))
        self.assertTrue(driver.find_element(By.ID, 'register_button'))
    def test_product_listing_page_elements(self):
        driver = self.driver
        self.login(driver)
        self.assertTrue(driver.find_element(By.ID, 'product_container'))
        self.assertTrue(driver.find_elements(By.CLASS_NAME, 'product_item'))
        self.assertTrue(driver.find_element(By.ID, 'add_to_cart_button'))
        self.assertTrue(driver.find_element(By.ID, 'cart_icon'))
    def test_shopping_cart_page_elements(self):
        driver = self.driver
        self.login(driver)
        driver.find_element(By.ID, 'cart_icon').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'cart_items_container'))
        self.assertTrue(driver.find_element(By.ID, 'checkout_button'))
        self.assertTrue(driver.find_element(By.ID, 'remove_item_button'))
    def test_checkout_page_elements(self):
        driver = self.driver
        self.login(driver)
        driver.find_element(By.ID, 'cart_icon').click()
        time.sleep(1)  # Wait for the page to load
        driver.find_element(By.ID, 'checkout_button').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'shipping_address_input'))
        self.assertTrue(driver.find_element(By.ID, 'payment_info_input'))
        self.assertTrue(driver.find_element(By.ID, 'confirm_order_button'))
    def test_order_confirmation_page_elements(self):
        driver = self.driver
        self.login(driver)
        driver.find_element(By.ID, 'cart_icon').click()
        time.sleep(1)  # Wait for the page to load
        driver.find_element(By.ID, 'checkout_button').click()
        time.sleep(1)  # Wait for the page to load
        driver.find_element(By.ID, 'confirm_order_button').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'order_summary_container'))
        self.assertTrue(driver.find_element(By.ID, 'continue_shopping_button'))
    def login(self, driver):
        driver.find_element(By.ID, 'username_input').send_keys(self.username)
        driver.find_element(By.ID, 'password_input').send_keys(self.password)
        driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the page to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
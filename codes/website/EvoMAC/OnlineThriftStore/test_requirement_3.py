'''
Test the elements and integrity of ALL pages in the OnlineThriftStore application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestOnlineThriftStore(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "john_doe"  # Example username
        self.password = "abcd1234"   # Example password
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'username_field'))
        self.assertTrue(driver.find_element(By.ID, 'password_field'))
        self.assertTrue(driver.find_element(By.ID, 'login_button'))
        self.assertTrue(driver.find_element(By.ID, 'error_message'))
        self.assertTrue(driver.find_element(By.ID, 'register_link'))
    def test_registration_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, 'register_link').click()
        time.sleep(1)  # Wait for the page to load
        self.assertTrue(driver.find_element(By.ID, 'register_username_field'))
        self.assertTrue(driver.find_element(By.ID, 'register_password_field'))
        self.assertTrue(driver.find_element(By.ID, 'confirm_password_field'))
        self.assertTrue(driver.find_element(By.ID, 'register_button'))
        self.assertTrue(driver.find_element(By.ID, 'registration_success_message'))
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'search_field'))
        self.assertTrue(driver.find_element(By.ID, 'search_button'))
        self.assertTrue(driver.find_element(By.ID, 'shopping_cart_button'))
        self.assertTrue(driver.find_element(By.ID, 'checkout_button'))
        self.assertTrue(driver.find_element(By.ID, 'sell_item_button'))
        self.assertTrue(driver.find_element(By.ID, 'user_profile_button'))
    def test_item_details_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'search_field').send_keys("cell phone" + Keys.RETURN)
        time.sleep(1)  # Wait for the search results to load
        driver.find_element(By.ID, 'search_button').click()
        time.sleep(1)  # Wait for the item details page to load
        self.assertTrue(driver.find_element(By.ID, 'item_title'))
        self.assertTrue(driver.find_element(By.ID, 'item_seller'))
        self.assertTrue(driver.find_element(By.ID, 'item_price'))
        self.assertTrue(driver.find_element(By.ID, 'item_status'))
        self.assertTrue(driver.find_element(By.ID, 'add_to_cart_button'))
        self.assertTrue(driver.find_element(By.ID, 'back_button'))
    def test_shopping_cart_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'shopping_cart_button').click()
        time.sleep(1)  # Wait for the shopping cart page to load
        self.assertTrue(driver.find_element(By.ID, 'cart_items_list'))
        self.assertTrue(driver.find_element(By.ID, 'remove_item_button'))
        self.assertTrue(driver.find_element(By.ID, 'total_price_display'))
        self.assertTrue(driver.find_element(By.ID, 'checkout_button'))
        self.assertTrue(driver.find_element(By.ID, 'back_button'))
    def test_checkout_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'shopping_cart_button').click()
        time.sleep(1)  # Wait for the shopping cart page to load
        driver.find_element(By.ID, 'checkout_button').click()
        time.sleep(1)  # Wait for the checkout page to load
        self.assertTrue(driver.find_element(By.ID, 'total_price_display'))
        self.assertTrue(driver.find_element(By.ID, 'payment_method_field'))
        self.assertTrue(driver.find_element(By.ID, 'confirm_purchase_button'))
        self.assertTrue(driver.find_element(By.ID, 'cancel_purchase_button'))
    def test_sell_item_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'sell_item_button').click()
        time.sleep(1)  # Wait for the sell item page to load
        self.assertTrue(driver.find_element(By.ID, 'item_title_field'))
        self.assertTrue(driver.find_element(By.ID, 'item_description_field'))
        self.assertTrue(driver.find_element(By.ID, 'item_price_field'))
        self.assertTrue(driver.find_element(By.ID, 'post_item_button'))
        self.assertTrue(driver.find_element(By.ID, 'cancel_button'))
    def test_user_profile_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, 'user_profile_button').click()
        time.sleep(1)  # Wait for the user profile page to load
        self.assertTrue(driver.find_element(By.ID, 'purchased_items_display'))
        self.assertTrue(driver.find_element(By.ID, 'on_sale_items_display'))
        self.assertTrue(driver.find_element(By.ID, 'logout_button'))
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, 'username_field').send_keys(self.username)
        driver.find_element(By.ID, 'password_field').send_keys(self.password)
        driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for the dashboard to load
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
import os
import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

sys.path.append(os.path.abspath('evaluator'))
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):

    def setUp(self):
        # Initialize the web driver (make sure to provide the proper path for your web driver)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        # Close the browser session
        self.driver.quit()

    def login(self):
        self.driver.delete_all_cookies()
        username = "john_doe"
        password = "abcd1234"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_elements(self):
        self.assertEqual(self.driver.title, "Login")
        self.driver.find_element(By.ID, "username_field")
        self.driver.find_element(By.ID, "password_field")
        self.driver.find_element(By.ID, "login_button")
        #self.driver.find_element(By.ID, "error_message")
        self.driver.find_element(By.ID, "register_link")

    def test_login_functionality(self):
        self.driver.find_element(By.ID, "username_field").send_keys("john_doe")
        self.driver.find_element(By.ID, "password_field").send_keys("abcd1234")
        self.driver.find_element(By.ID, "login_button").click()
        self.assertIn("Dashboard", self.driver.title)

    # Registration Page Tests
    def test_registration_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        self.driver.find_element(By.ID, "register_username_field")
        self.driver.find_element(By.ID, "register_password_field")
        self.driver.find_element(By.ID, "confirm_password_field")
        self.driver.find_element(By.ID, "register_button")
        #self.driver.find_element(By.ID, "registration_success_message")

    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()

        username = "newuser"
        password = "newpassword"

        self.driver.find_element(By.ID, "register_username_field").send_keys(username)
        self.driver.find_element(By.ID, "register_password_field").send_keys(password)
        self.driver.find_element(By.ID, "confirm_password_field").send_keys(password)
        self.driver.find_element(By.ID, "register_button").click()

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username}:{password}\n" in users)

    # Dashboard Page Tests
    def test_dashboard_elements(self):
        self.login()
        self.assertIn("Dashboard", self.driver.title)
        self.driver.find_element(By.ID, "search_field")
        self.driver.find_element(By.ID, "search_button")
        self.driver.find_element(By.ID, "shopping_cart_button")
        self.driver.find_element(By.ID, "checkout_button")
        self.driver.find_element(By.ID, "sell_item_button")
        self.driver.find_element(By.ID, "user_profile_button")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "shopping_cart_button").click()
        self.assertIn('Shopping Cart', self.driver.title)
    
        self.login()
        self.driver.find_element(By.ID, "sell_item_button").click()
        self.assertIn('Sell Item', self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "user_profile_button").click()
        self.assertIn('User Profile', self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "user_profile_button").click()
        self.assertIn('User Profile', self.driver.title) 
        self.driver.find_element(By.ID, "search_field").send_keys("cell phone")
        self.driver.find_element(By.ID, "search_button").click()
        self.assertIn("cell phone", self.driver.title)

    # Item Details Page Tests
    def test_item_details_elements(self):
        self.login()
        self.driver.find_element(By.ID, "search_field").send_keys("cell phone")
        self.driver.find_element(By.ID, "search_button").click()
        # Assuming an item exists for test purposes
        self.driver.find_element(By.ID, "item_title")
        self.driver.find_element(By.ID, "item_seller")
        self.driver.find_element(By.ID, "item_price")
        self.driver.find_element(By.ID, "item_status")
        self.driver.find_element(By.ID, "add_to_cart_button")
        self.driver.find_element(By.ID, "back_button")

    def test_item_details_functionality(self):
        self.login()
        # Assuming an item exists for test purposes
        self.driver.find_element(By.ID, "search_field").send_keys("cell phone")
        self.driver.find_element(By.ID, "search_button").click()
        self.driver.find_element(By.ID, "add_to_cart_button").click()

        with open(os.path.join('data', 'carts.txt'), 'r') as f:
            cart_items = f.readlines()
            self.assertIn("john_doe|cell phone\n", cart_items)

        self.login()
        # Assuming an item exists for test purposes
        self.driver.find_element(By.ID, "search_field").send_keys("cell phone")
        self.driver.find_element(By.ID, "search_button").click()
        self.driver.find_element(By.ID, "back_button").click()
        self.assertIn("Dashboard", self.driver.title)

    # Shopping Cart Page Tests
    def test_shopping_cart_elements(self):
        self.login()
        self.driver.find_element(By.ID, "shopping_cart_button").click()
        self.driver.find_element(By.ID, "cart_items_list")
        self.driver.find_element(By.ID, "remove_item_button")
        self.driver.find_element(By.ID, "total_price_display")
        self.driver.find_element(By.ID, "checkout_button")
        self.driver.find_element(By.ID, "back_button")

    def test_shopping_cart_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "shopping_cart_button").click()
        # Get the entire cart as a single text block
        cart_text = self.driver.find_element(By.ID, "cart_items_list").text

        # Determine which item comes first in the cart, 'jacket' or 'cell phone'
        if "jacket" in cart_text and "cell phone" in cart_text:
            if cart_text.index("jacket") < cart_text.index("cell phone"):
                # 'Jacket' comes first
                first_item = "jacket"
            else:
                # 'Cell phone' comes first
                first_item = "cell phone"
        elif "jacket" in cart_text:
            first_item = "jacket"
        elif "cell phone" in cart_text:
            first_item = "cell phone"
        else:
            self.fail("Neither 'jacket' nor 'cell phone' is found in the cart.")

        # Remove the first item in the list
        self.driver.find_element(By.ID, "remove_item_button").click()

        # Check if the removed item is indeed gone from the cart
        with open(os.path.join('data', 'carts.txt'), 'r') as f:
            cart_items = f.readlines()
            for line in cart_items:
                self.assertNotIn(first_item, line)

        # Optionally, verify the cart on the page to ensure the item is no longer listed
        self.login()
        self.driver.find_element(By.ID, "shopping_cart_button").click()
        updated_cart_text = self.driver.find_element(By.ID, "cart_items_list").text
        self.assertNotIn(first_item, updated_cart_text)

        self.login()
        self.driver.find_element(By.ID, "shopping_cart_button").click()
        self.driver.find_element(By.ID, "checkout_button").click()
        self.assertIn("Checkout", self.driver.title)

    # Checkout Page Tests
    def test_checkout_elements(self):
        self.login()
        self.driver.find_element(By.ID, "shopping_cart_button").click()
        self.driver.find_element(By.ID, "checkout_button").click()
        self.driver.find_element(By.ID, "total_price_display")
        self.driver.find_element(By.ID, "payment_method_field")
        self.driver.find_element(By.ID, "confirm_purchase_button")
        self.driver.find_element(By.ID, "cancel_purchase_button")

    def test_checkout_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "shopping_cart_button").click()
        cart_text = self.driver.find_element(By.ID, "cart_items_list").text
        if "cell phone" in cart_text:
            item = "cell phone"
        elif "jacket" in cart_text:
            item = "jacket"
        else:
            self.fail("Neither 'jacket' nor 'cell phone' is found in the cart.")

        self.driver.find_element(By.ID, "checkout_button").click()
        self.driver.find_element(By.ID, "payment_method_field").send_keys("credit card")
        self.driver.find_element(By.ID, "confirm_purchase_button").click()

        with open(os.path.join('data', 'sold.txt'), 'r') as f:
            purchased_items = f.readlines()
            if item == "cell phone":
                self.assertIn("john_doe|cell phone|A brand new cell phone.|500.00|jane_smith\n", purchased_items)
            elif item == "jacket":
                self.assertIn("john_doe|jacket|Stylish jacket, barely worn.|30.00|jane_smith\n", purchased_items)

        with open(os.path.join('data', 'on_sale.txt'), 'r') as f:
            sale_items = f.readlines()
            if item == "cell phone":
                self.assertNotIn("cell phone|A brand new cell phone.|500.00|jane_smith\n", purchased_items)
            elif item == "jacket":
                self.assertNotIn("jacket|Stylish jacket, barely worn.|30.00|jane_smith\n", purchased_items)

    # Sell Item Page Tests
    def test_sell_item_elements(self):
        self.login()
        self.driver.find_element(By.ID, "sell_item_button").click()
        self.driver.find_element(By.ID, "item_title_field")
        self.driver.find_element(By.ID, "item_description_field")
        self.driver.find_element(By.ID, "item_price_field")
        self.driver.find_element(By.ID, "post_item_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_sell_item_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "sell_item_button").click()
        self.driver.find_element(By.ID, "item_title_field").send_keys("New Item")
        self.driver.find_element(By.ID, "item_description_field").send_keys("A description of the new item.")
        self.driver.find_element(By.ID, "item_price_field").send_keys("100.00")
        self.driver.find_element(By.ID, "post_item_button").click()

        with open(os.path.join('data', 'on_sale.txt'), 'r') as f:
            items = f.readlines()
            self.assertIn("New Item|A description of the new item.|100.00|john_doe\n", items)

    # User Profile Page Tests
    def test_user_profile_elements(self):
        self.login()
        self.driver.find_element(By.ID, "user_profile_button").click()
        self.driver.find_element(By.ID, "purchased_items_display")
        self.driver.find_element(By.ID, "on_sale_items_display")
        self.driver.find_element(By.ID, "logout_button")

    def test_user_profile_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "user_profile_button").click()
        purchased_items = self.driver.find_element(By.ID, "purchased_items_display").text
        self.assertIn("laptop", purchased_items)

        on_sale_items = self.driver.find_element(By.ID, "on_sale_items_display").text
        self.assertIn("lamp", on_sale_items)

        self.driver.find_element(By.ID, "logout_button").click()
        self.assertIn("Login", self.driver.title)

class TestOnlineThriftStore:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        if not os.path.exists('data'):
            shutil.copytree(f'{code_path}/data', 'data')
        else:
            shutil.rmtree('data')
            shutil.copytree(f'{code_path}/data', 'data')

        self.checker = checker
        self.time = time
        self.py = path
        self.pid = get_python_pid()

    def test_set_up(self):
        try:
            self.process = subprocess.Popen(['python', f'{self.py}'])
            time.sleep(self.time)
        except:
            return 0
        return 1

    def tear_down(self):
        if os.path.exists('data'):
            shutil.rmtree('data')
        self.process.terminate()

        pid = get_python_pid()
        for p in pid:
            if p not in self.pid:
                proc = psutil.Process(p)
                proc.terminate()

    def main(self):
        result = {
            'total': 17,
            'total_basic': 9,
            'total_advanced': 8,
            'basic': 0,
            'advanced': 0,
            'test_cases': {
                'set_up': 0
            }
        }
        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except:
            self.tear_down()

        if result['test_cases']['set_up'] == 1:
            try:
                test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
                res = CustomTestRunner().run(test_suite)
            except:
                print("ERROR")
        self.tear_down()

        for test in res['succ']:
            test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
            result['test_cases'][test_cases] = 1
        for test in res['fail']:
            test_cases = "_".join(str(test).split(" ")[0].split('_')[1:])
            result['test_cases'][test_cases] = 0

        result['basic'] += 1

        for item in result['test_cases']:
            if 'elements' in item:
                result['basic'] += result['test_cases'][item]
            if 'functionality' in item:
                result['advanced'] += result['test_cases'][item]

        return result


if __name__ == '__main__':
    checker = None
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-0\OnlineThriftStore\app.py'
    test = TestOnlineThriftStore(checker, py)
    print(test.main())


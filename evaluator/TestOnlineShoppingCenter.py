import psutil
import shutil
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import subprocess
import sys

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid



class TestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the webdriver (assuming Chrome is being used)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")  # Start from the landing page

    def tearDown(self):
        self.driver.quit()  # Close the browser after each test

    def login(self):
        self.driver.delete_all_cookies()
        username = "johndoe"
        password = "secret123"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    def test_login_elements(self):
        """Checks presence and accessibility of critical elements on the Login Page."""
        self.assertEqual(self.driver.title, "User Login")
        self.driver.find_element(By.ID, "username_input")
        self.driver.find_element(By.ID, "password_input")
        self.driver.find_element(By.ID, "login_button")
        self.driver.find_element(By.ID, "register_link")

    def test_login_functionality(self):
        """Tests the login functionality."""
        # Assuming a known user for testing

        username = "johndoe"
        password = "secret123"
        
        # Performing login
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

        # Check if redirected to the Product Listing Page by checking the title
        self.assertEqual(self.driver.title, "Product Listing")

        # Check if redirected to the User Registration Page by checking the title
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()
        self.assertEqual(self.driver.title, "User Registration")


    def test_registration_elements(self):
        """Checks presence and accessibility of critical elements on the Registration Page."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()

        self.driver.find_element(By.ID, "reg_username_input")
        self.driver.find_element(By.ID, "reg_password_input")
        self.driver.find_element(By.ID, "reg_email_input")
        self.driver.find_element(By.ID, "register_button")
        
    def test_registration_functionality(self):
        """Tests the user registration functionality."""
        # Navigating to Registration Page
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_link").click()

        # Registering a new user
        username = "newuser"
        password = "newpassword"
        email = "newuser@example.com"

        self.driver.find_element(By.ID, "reg_username_input").send_keys(username)
        self.driver.find_element(By.ID, "reg_password_input").send_keys(password)
        self.driver.find_element(By.ID, "reg_email_input").send_keys(email)
        self.driver.find_element(By.ID, "register_button").click()

        # Validate that the user has been added to users.txt
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username},{password},{email}\n" in users)

    def test_product_listing_elements(self):
        """Checks presence and accessibility of critical elements on the Product Listing Page."""
        # Must navigate from the landing page to the Product Listing Page
        self.login()  # Log in to reach the product listing
        self.driver.find_element(By.ID, "product_container")
        self.driver.find_element(By.CLASS_NAME, "product_item")
        self.driver.find_element(By.ID, "add_to_cart_button")
        self.driver.find_element(By.ID, "cart_icon")

    def test_product_listing_functionality(self):
        """Tests adding a product to the shopping cart."""
        # Must navigate from the landing page to the Product Listing Page
        self.login()  # Log in to reach the product listing

        # Adding a known product (assuming product ID 001 exists)
        self.driver.find_element(By.ID, "add_to_cart_button").click()

        # Assuming the product ID to verify is from products.txt
        with open(os.path.join('data', 'shopping_cart.txt'), 'r') as f:
            cart_items = f.readlines()
            print(cart_items)
            self.assertTrue(f"johndoe,001,3\n" in cart_items)

         # Check if redirected to the Product Listing Page by checking the title
        self.driver.find_element(By.ID, "cart_icon").click()
        self.assertEqual(self.driver.title, "Shopping Cart")

    def test_shopping_cart_elements(self):
        """Checks presence and accessibility of critical elements on the Shopping Cart Page."""
        # Must navigate from the landing page to the Shopping Cart Page
        self.login()  
        self.driver.find_element(By.ID, "cart_icon").click() # Ensure item is added to cart
        self.driver.find_element(By.ID, "cart_items_container")
        self.driver.find_element(By.ID, "checkout_button")
        self.driver.find_element(By.ID, "remove_item_button")

    def test_shopping_cart_functionality(self):
        """Tests checkout functionality from the shopping cart."""
        # Must navigate from the landing page to the Shopping Cart Page
        self.login()  
        self.driver.find_element(By.ID, "cart_icon").click() # Ensure item is added to cart

        # Proceeding to remove_item
        with open(os.path.join('data', 'shopping_cart.txt'), 'r') as f:
            cart_items = f.readlines()
        previous_cart = len(cart_items)
        self.driver.find_element(By.ID, "remove_item_button").click()
        with open(os.path.join('data', 'shopping_cart.txt'), 'r') as f:
            cart_items = f.readlines()
        current_cart = len(cart_items)
        self.assertEqual(previous_cart - current_cart, 1)

        # Proceeding to checkout
        self.driver.find_element(By.ID, "checkout_button").click()
        self.assertEqual(self.driver.title, "Checkout")

    def test_checkout_elements(self):
        self.login()  
        self.driver.find_element(By.ID, "cart_icon").click()
        self.driver.find_element(By.ID, "checkout_button").click()

        self.driver.find_element(By.ID, "shipping_address_input")
        self.driver.find_element(By.ID, "payment_info_input")
        self.driver.find_element(By.ID, "confirm_order_button")
    
    def test_checkout_functionality(self):
        self.login()  
        self.driver.find_element(By.ID, "cart_icon").click()
        self.driver.find_element(By.ID, "checkout_button").click()

        # Providing shipping address and payment info
        shipping_address = "123 Main St"
        payment_info = "4111111111111111"  # Sample card number

        self.driver.find_element(By.ID, "shipping_address_input").send_keys(shipping_address)
        self.driver.find_element(By.ID, "payment_info_input").send_keys(payment_info)
        self.driver.find_element(By.ID, "confirm_order_button").click()

        # Confirming that the order was placed successfully by checking for Order Summary
        self.assertIn("Order Confirmation", self.driver.title)

    def test_order_confirmation_elements(self):
        """Checks presence and accessibility of critical elements on the Order Confirmation Page."""
        # Must navigate from the landing page to the Order Confirmation Page
        self.login()  
        self.driver.find_element(By.ID, "cart_icon").click()
        self.driver.find_element(By.ID, "checkout_button").click()  
        shipping_address = "123 Main St"
        payment_info = "4111111111111111"  # Sample card number

        self.driver.find_element(By.ID, "shipping_address_input").send_keys(shipping_address)
        self.driver.find_element(By.ID, "payment_info_input").send_keys(payment_info)
        self.driver.find_element(By.ID, "confirm_order_button").click() # Ensure order is confirmed
        self.driver.find_element(By.ID, "order_summary_container")
        self.driver.find_element(By.ID, "continue_shopping_button")

    def test_order_confirmation_functionality(self):
        """Tests the functionality of continuing shopping after an order confirmation."""
        # Must navigate from the landing page to the Order Confirmation Page
        self.login()  
        self.driver.find_element(By.ID, "cart_icon").click()
        self.driver.find_element(By.ID, "checkout_button").click()  
        shipping_address = "123 Main St"
        payment_info = "4111111111111111"  # Sample card number
        self.driver.find_element(By.ID, "shipping_address_input").send_keys(shipping_address)
        self.driver.find_element(By.ID, "payment_info_input").send_keys(payment_info)
        self.driver.find_element(By.ID, "confirm_order_button").click() # Ensure order is confirmed

        div_text = self.driver.find_element(By.ID, "order_summary_container").text

        self.assertIn(shipping_address, div_text)
        self.assertIn(payment_info, div_text)

        # Continuing shopping
        self.driver.find_element(By.ID, "continue_shopping_button").click()
        # Verify we returned to the Product Listing
        self.assertEqual(self.driver.title, "Product Listing")

class TestOnlineShoppingCenter:
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
            'total': 13,
            'total_basic': 7,
            'total_advanced': 6,
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
            try :
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-2\OnlineShoppingCenter\app.py'
    test = TestOnlineShoppingCenter(checker, py)
    print(test.main())
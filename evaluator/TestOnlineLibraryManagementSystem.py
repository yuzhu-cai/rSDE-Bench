import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):
    def setUp(self):
        # Initialize a new web session for each test
        self.driver = webdriver.Chrome()  # Use the appropriate WebDriver for your browser
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        # Close the web session after each test
        self.driver.quit()

    def login(self):
        self.driver.delete_all_cookies()
        username = "johndoe"
        password = "password123"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "login_username").send_keys(username)
        self.driver.find_element(By.ID, "login_password").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Test Login Page
    def test_login_elements(self):
        self.assertEqual(self.driver.title, "Login")
        self.driver.find_element(By.ID, "login_username")
        self.driver.find_element(By.ID, "login_password")
        self.driver.find_element(By.ID, "login_button")
        #self.driver.find_element(By.ID, "login_error")
        self.driver.find_element(By.ID, "register_button")


    def test_login_functionality(self):

        self.driver.find_element(By.ID, "login_username").send_keys("johndoe")
        self.driver.find_element(By.ID, "login_password").send_keys("password123")
        self.driver.find_element(By.ID, "login_button").click()

        self.assertEqual(self.driver.title, "Dashboard")

        # Check if redirected to the User Registration Page by checking the title
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()
        self.assertEqual(self.driver.title, "Register")
    
    # Test Register Page
    def test_registration_elements(self):
        """Test the presence and accessibility of Registration Page elements."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()

        self.driver.find_element(By.ID, "reg_username_input")
        self.driver.find_element(By.ID, "reg_password_input")
        self.driver.find_element(By.ID, "reg_email_input")
        self.driver.find_element(By.ID, "register_message")
        self.driver.find_element(By.ID, "register_button")

    def test_registration_functionality(self):
        """Test Registration Page functionality."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()

        # Registering a new user
        username = "newuser"
        password = "newpassword"
        email = "newuser@example.com"

        self.driver.find_element(By.ID, "reg_username_input").send_keys(username)
        self.driver.find_element(By.ID, "reg_password_input").send_keys(password)
        self.driver.find_element(By.ID, "reg_email_input").send_keys(email)
        self.driver.find_element(By.ID, "register_button").click()

        # Check if redirected to Main Blog Page
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username}|{password}\n" in users)

    # Test Dashboard Page
    def test_dashboard_elements(self):
        self.login()  # Ensure we're logged in
        welcome_message = self.driver.find_element(By.ID, "dashboard_welcome")
        self.assertIn("Welcome", welcome_message.text)

        self.driver.find_element(By.ID, "dashboard_welcome")
        self.driver.find_element(By.ID, "dashboard_view_books")
        self.driver.find_element(By.ID, "dashboard_manage_users")
        self.driver.find_element(By.ID, "dashboard_search_books")
        self.driver.find_element(By.ID, "dashboard_logout")

    def test_dashboard_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "dashboard_view_books").click()
        self.assertIn("Manage Books", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "dashboard_manage_users").click()
        self.assertIn("Manage Users", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "dashboard_search_books").click()
        self.assertIn("Search Books", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "dashboard_logout").click()
        self.assertIn("Logout", self.driver.title)

    # Test Book Management Page
    def test_book_management_elements(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_view_books").click()

        self.driver.find_element(By.ID, "manage_books_form")
        self.driver.find_element(By.ID, "add_book_title")
        self.driver.find_element(By.ID, "add_book_author")
        self.driver.find_element(By.ID, "add_book_isbn")
        self.driver.find_element(By.ID, "save_book_button")
        self.driver.find_element(By.ID, "delete_book_button")
        self.driver.find_element(By.ID, "book_list")

    def test_book_management_functionality(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_view_books").click()

        self.driver.find_element(By.ID, "add_book_title").send_keys("The Great Gatsby")
        self.driver.find_element(By.ID, "add_book_author").send_keys("F. Scott Fitzgerald")
        self.driver.find_element(By.ID, "add_book_isbn").send_keys("9780743273565")
        self.driver.find_element(By.ID, "save_book_button").click()

        with open(os.path.join('data', 'books.txt'), 'r') as file:
            books = file.readlines()
            self.assertIn("The Great Gatsby|F. Scott Fitzgerald|9780743273565\n", books)
        previous = len(books)

        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_view_books").click()
        self.driver.find_element(By.ID, "delete_book_button").click()
        with open(os.path.join('data', 'books.txt'), 'r') as file:
            books = file.readlines()
        current = len(books)
        self.assertEqual(previous - current, 1)

    # Test User Management Page
    def test_user_management_elements(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_manage_users").click()

        self.driver.find_element(By.ID, "manage_users_form")
        self.driver.find_element(By.ID, "add_user_username")
        self.driver.find_element(By.ID, "add_user_password")
        self.driver.find_element(By.ID, "save_user_button")
        self.driver.find_element(By.ID, "user_list")

    def test_user_management_functionality(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_manage_users").click()

        current_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") 
        name = f"testuser {current_time}"
        pwd = f'password456-{current_time}'
        self.driver.find_element(By.ID, "add_user_username").send_keys(name)
        self.driver.find_element(By.ID, "add_user_password").send_keys(pwd)
        self.driver.find_element(By.ID, "save_user_button").click()

        with open(os.path.join('data', 'users.txt'), 'r') as file:
            users = file.readlines()
            self.assertIn(f"{name}|{pwd}\n", users)

    # Test Search Page
    def test_search_elements(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_search_books").click()

        self.driver.find_element(By.ID, "search_field")
        self.driver.find_element(By.ID, "search_button")
        self.driver.find_element(By.ID, "search_results")

    def test_search_functionality(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_search_books").click()

        self.driver.find_element(By.ID, "search_field").send_keys("The Great Gatsby")
        self.driver.find_element(By.ID, "search_button").click()

        results = self.driver.find_element(By.ID, "search_results").text
        self.assertIn("The Great Gatsby", results)

    # Test Logout Page
    def test_logout_elements(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_logout").click()

        self.driver.find_element(By.ID, "logout_message")
        self.driver.find_element(By.ID, "logout_redirect")

    def test_logout_functionality(self):
        self.login()  # Ensure we're on the dashboard
        self.driver.find_element(By.ID, "dashboard_logout").click()
        self.driver.find_element(By.ID, "logout_redirect").click()
        self.assertIn("Login", self.driver.title)


class TestOnlineLibraryManagementSystem:
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
            'total': 15,
            'total_basic': 8,
            'total_advanced': 7,
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-0\OnlineLibraryManagementSystem\app.py'
    test = TestOnlineLibraryManagementSystem(checker, py)
    print(test.main())
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
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
        # Initialize the Selenium WebDriver
        self.driver = webdriver.Chrome()  # Ensure you have the right driver for your browser
        self.driver.get("http://localhost:5000")  # Start from the landing page
    
    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()
    def login(self):
        driver = self.driver
        username = "user1"  # Replace with a valid username from Users.txt
        password = "abc123"  # Replace with valid password hash
        driver.find_element(By.ID, "username_input").send_keys(username)
        driver.find_element(By.ID, "password_input").send_keys(password)
        driver.find_element(By.ID, "login_button").click()
    # Login Page Tests
    def test_login_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "username_input")
        driver.find_element(By.ID, "password_input")
        driver.find_element(By.ID, "login_button")
        driver.find_element(By.ID, "about_button")
    def test_login_page_functionality(self):
        driver = self.driver
        username = "user1"  # Replace with a valid username from Users.txt
        password = "abc123"  # Replace with valid password hash
        driver.find_element(By.ID, "username_input").send_keys(username)
        driver.find_element(By.ID, "password_input").send_keys(password)
        driver.find_element(By.ID, "login_button").click()
        time.sleep(1)
        self.assertIn("Home", driver.title)  # Verify redirection to Home page

    # Home Page Tests
    def test_home_page_elements(self):
        self.login()  # Ensure we're logged in
        time.sleep(1)  # Wait for home page load
        self.assertTrue(self.driver.find_element(By.ID, 'quotes_display').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add_quote_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'favorites_button').is_displayed())
    
    def test_home_page_functionality(self):
        self.login()  # Ensure we're logged in
        time.sleep(1)  # Wait for home page load
        # Ensure quotes are displayed in the quotes section
        quotes_display = self.driver.find_element(By.ID, 'quotes_display')
        self.assertTrue(quotes_display.is_displayed())
        # Read from Quotes.txt, then check against displayed contents (pseudo-implementation)
        with open('data/Quotes.txt', 'r') as f:
            quotes = f.readlines()
        for i, quote in enumerate(quotes):
            quote_text, author = quote.strip().split('|')
            self.assertIn(f'{quote_text} - {author}', quotes_display.text)

    # Add Quote Page Tests
    def test_add_quote_page_elements(self):
        self.login()  # Ensure we're on Home page
        self.driver.find_element(By.ID, 'add_quote_button').click()
        time.sleep(1)  # Wait for page load
        self.assertTrue(self.driver.find_element(By.ID, 'quote_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'author_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'submit_quote_button').is_displayed())
    
    def test_add_quote_page_functionality(self):
        self.login()  # Ensure we're on Home page
        self.driver.find_element(By.ID, 'add_quote_button').click()
        quote = "New quote for testing."
        author = "Test Author"
        self.driver.find_element(By.ID, 'quote_input').send_keys(quote)
        self.driver.find_element(By.ID, 'author_input').send_keys(author)
        self.driver.find_element(By.ID, 'submit_quote_button').click()
        time.sleep(1)  # Wait for redirect back to home
        # Verify user registration by checking user data file
        with open(os.path.join('data', 'Quotes.txt'), 'r') as file:
            users = file.readlines()
        exists = any("New quote for testing.|Test Author" in line for line in users)
        self.assertTrue(exists)


    
    # Edit Quote Page Tests
    def test_edit_quote_page_elements(self):
        self.login()  # Ensure we're on Home page
        # Assume at least one quote exists for editing
        self.driver.find_element(By.ID, 'edit_quote_0').click()  # Edit the first quote
        self.assertTrue(self.driver.find_element(By.ID, 'edit_quote_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'edit_author_input').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'update_quote_button').is_displayed())

    def test_edit_quote_page_functionality(self):
        self.login()  # Ensure we're on Home page
        # Assume at least one quote exists for editing
        self.driver.find_element(By.ID, 'edit_quote_0').click()  # Edit the first quote
        new_quote = "Updated quote for testing."
        new_author = "Updated Author"
        self.driver.find_element(By.ID, 'edit_quote_input').clear()
        self.driver.find_element(By.ID, 'edit_author_input').clear()
        self.driver.find_element(By.ID, 'edit_quote_input').send_keys(new_quote)
        self.driver.find_element(By.ID, 'edit_author_input').send_keys(new_author)
        self.driver.find_element(By.ID, 'update_quote_button').click()
        with open(os.path.join('data', 'Quotes.txt'), 'r') as file:
            users = file.readlines()
        exists = any("Updated quote for testing.|Updated Author" in line for line in users)
        self.assertTrue(exists)

    # Delete Quote Confirmation Page Tests
    def test_delete_confirmation_page_elements(self):
        self.login()  # Ensure we're on Home page
        self.driver.find_element(By.ID, 'delete_quote_1').click()  # Click delete for the first quote
        self.assertTrue(self.driver.find_element(By.ID, 'confirm_message').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'confirm_deletion_button').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'cancel_button').is_displayed())

    def test_delete_confirmation_page_functionality(self):
        self.login()  # Ensure we're on Home page
        self.driver.find_element(By.ID, 'delete_quote_1').click()  # Click delete for the first quote
        initial_quote = "Quote to be deleted."  # Assuming we know the quote is at index 0
        self.driver.find_element(By.ID, 'confirm_deletion_button').click()
        
        # Verify user registration by checking user data file
        with open(os.path.join('data', 'users.txt'), 'r') as file:
            users = file.readlines()
        exists = not any("Success is not the key to happiness. Happiness is the key to success.|Albert Schweitzer" in line for line in users)
        self.assertTrue(exists)


    # Favorites Page Tests
    def test_favorites_page_elements(self):
        self.login()  # Ensure we're on Home page
        self.driver.find_element(By.ID, 'favorites_button').click()
        self.assertTrue(self.driver.find_element(By.ID, 'favorites_display').is_displayed())

    def test_favorites_page_functionality(self):
        self.login()  # Ensure we're on Home page
        self.driver.find_element(By.ID, 'favorites_button').click()        # Check favorites from Favorites.txt
        with open('data/Favorites.txt', 'r') as f:
            favorites = f.readlines()
        favorites_display = self.driver.find_element(By.ID, 'favorites_display').text
        for favorite in favorites:
            _, quote_text, author = favorite.strip().split('|')
            self.assertIn(f'{quote_text} - {author}', favorites_display)

    # About Page Tests
    def test_about_page_elements(self):
        self.driver.find_element(By.ID, 'about_button').click()
        self.assertTrue(self.driver.find_element(By.ID, 'app_description').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'developer_info').is_displayed())

    def test_about_page_functionality(self):
        self.driver.find_element(By.ID, 'about_button').click()
        self.assertTrue(self.driver.find_element(By.ID, 'app_description').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'developer_info').is_displayed())

class TestMotivationalQuotesApp:
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
    py = r'D:\research\asie-bench_withweb\codes\gpt-4o-mini-1\MotivationalQuotesApp\app.py'
    test = TestMotivationalQuotesApp(checker, py)
    print(test.main())






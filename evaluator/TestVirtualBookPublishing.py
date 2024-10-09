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
        self.driver = webdriver.Chrome()  # Initialize Chrome WebDriver
        self.driver.get("http://localhost:5000")  # Navigate to the landing page

    def tearDown(self):
        self.driver.quit()  # Close the browser after each test

    # Login Page Tests
    def test_loginPage_elements(self):
        driver = self.driver

        # Test for the presence of critical elements
        self.assertTrue(driver.find_element(By.ID, "username").is_displayed(), "Username field not found")
        self.assertTrue(driver.find_element(By.ID, "password").is_displayed(), "Password field not found")
        self.assertTrue(driver.find_element(By.ID, "loginBtn").is_displayed(), "Login button not found")
        self.assertTrue(driver.find_element(By.ID, "registrationLink").is_displayed(), "Registration link not found")
        self.assertTrue(driver.find_element(By.ID, "aboutLink").is_displayed(), "About link not found")

    def test_loginPage_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  

        self.assertIn("Dashboard", driver.title)  # Check if navigated to dashboard

    # Registration Page Tests
    def test_registrationPage_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "registrationLink").click()  # Navigate to Registration Page

        self.assertTrue(driver.find_element(By.ID, "regUsername").is_displayed(), "Registration Username field not found")
        self.assertTrue(driver.find_element(By.ID, "regPassword").is_displayed(), "Registration Password field not found")
        self.assertTrue(driver.find_element(By.ID, "regSubmit").is_displayed(), "Registration Submit button not found")

    def test_registrationPage_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, "registrationLink").click()  
        driver.find_element(By.ID, "regUsername").send_keys("newuser")
        driver.find_element(By.ID, "regPassword").send_keys("newpassword")
        driver.find_element(By.ID, "regSubmit").click()  

        # Verify user registration by checking user data file
        with open(os.path.join('data', 'users.txt'), 'r') as file:
            users = file.readlines()
        exists = any("newuser|newpassword" in line for line in users)
        self.assertTrue(exists)

    # Dashboard Page Tests
    def test_dashboardPage_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  

        self.assertTrue(driver.find_element(By.ID, "createBookBtn").is_displayed(), "Create New Book button not found")
        self.assertTrue(driver.find_element(By.ID, "viewBooksBtn").is_displayed(), "View My Books button not found")

    def test_dashboardPage_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  
        
        driver.find_element(By.ID, "createBookBtn").click()  # Navigate to Create New Book Page
        self.assertIn("Create New Book", driver.title)
        driver.find_element(By.ID, "cancelCreate").click()  # Navigate to Create New Book Page
        self.assertIn("Dashboard", driver.title)
        driver.find_element(By.ID, "viewBooksBtn").click()  # Navigate to Create New Book Page
        self.assertIn("My Books", driver.title)        

        # driver.find_element(By.ID, "bookTitle").send_keys("Sample Book")
        # driver.find_element(By.ID, "bookAuthor").send_keys("Sample Author")
        # driver.find_element(By.ID, "bookContent").send_keys("This is a sample book content.")
        # driver.find_element(By.ID, "submitBook").click()  

        # time.sleep(1)  # Wait for save process to finish
        # driver.find_element(By.ID, "viewBooksBtn").click()  # Check for new book in My Books
        # self.assertTrue(driver.find_element(By.ID, "booksList").is_displayed(), "Books list not displayed")

    # Create New Book Page Tests
    def test_createNewBookPage_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  
        
        driver.find_element(By.ID, "createBookBtn").click()
        
        self.assertTrue(driver.find_element(By.ID, "bookTitle").is_displayed(), "Book Title field not found")
        self.assertTrue(driver.find_element(By.ID, "bookAuthor").is_displayed(), "Book Author field not found")
        self.assertTrue(driver.find_element(By.ID, "bookContent").is_displayed(), "Book Content area not found")
        self.assertTrue(driver.find_element(By.ID, "submitBook").is_displayed(), "Submit button not found")
        self.assertTrue(driver.find_element(By.ID, "cancelCreate").is_displayed(), "Cancel button not found")

    def test_createNewBookPage_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  
        
        driver.find_element(By.ID, "createBookBtn").click()
        driver.find_element(By.ID, "bookTitle").send_keys("Test Book")
        driver.find_element(By.ID, "bookAuthor").send_keys("Test Author")
        driver.find_element(By.ID, "bookContent").send_keys("This is a test book content.")
        driver.find_element(By.ID, "submitBook").click()  

            
        saved_books = []
        with open('data/books.txt', 'r') as file:
            saved_books = [line.split('|')[0] for line in file.readlines()]

        self.assertIn("Test Book", saved_books, "Test Book not found in saved books")

    # View My Books Page Tests
    def test_viewMyBooksPage_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  
        
        driver.find_element(By.ID, "viewBooksBtn").click()
        self.assertTrue(driver.find_element(By.ID, "booksList").is_displayed(), "Books list not displayed")

    def test_viewMyBooksPage_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  
        
        driver.find_element(By.ID, "viewBooksBtn").click()  
        
        first_book_button = driver.find_element(By.ID, "viewBook_0")
        first_book_button.click()

        self.assertIn("Book Details", driver.title) 
        # self.assertTrue(driver.find_element(By.ID, "detailTitle").is_displayed(), "Title not displayed")
        # self.assertTrue(driver.find_element(By.ID, "detailAuthor").is_displayed(), "Author not displayed")
        # self.assertTrue(driver.find_element(By.ID, "detailContent").is_displayed(), "Content not displayed")

    # View Book Details Page Tests
    def test_viewBookDetailsPage_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  
        
        driver.find_element(By.ID, "viewBooksBtn").click()  
        
        driver.find_element(By.ID, "viewBook_0").click()  
        self.assertTrue(driver.find_element(By.ID, "detailTitle").is_displayed(), "Detail Title not displayed")
        self.assertTrue(driver.find_element(By.ID, "detailAuthor").is_displayed(), "Detail Author not displayed")
        self.assertTrue(driver.find_element(By.ID, "detailContent").is_displayed(), "Detail Content not displayed")
        self.assertTrue(driver.find_element(By.ID, "backToMyBooks").is_displayed(), "Back button not displayed")
    
    def test_viewBookDetailsPage_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys("username1")
        driver.find_element(By.ID, "password").send_keys("password1")
        driver.find_element(By.ID, "loginBtn").click()  
        
        driver.find_element(By.ID, "viewBooksBtn").click()  
        
        driver.find_element(By.ID, "viewBook_0").click()  
        
        driver.find_element(By.ID, "backToMyBooks").click()  
        self.assertTrue(driver.find_element(By.ID, "booksList").is_displayed(), "Failed to return to My Books Page")

    # About Page Tests
    def test_aboutPage_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "aboutLink").click()  
        self.assertTrue(driver.find_element(By.ID, "appDescription").is_displayed(), "App Description not found")
        self.assertTrue(driver.find_element(By.ID, "versionInfo").is_displayed(), "Version Info not found")
        self.assertTrue(driver.find_element(By.ID, "contactInfo").is_displayed(), "Contact Information not found")

    def test_aboutPage_functionality(self):
        driver = self.driver
        driver.find_element(By.ID, "aboutLink").click()  
        self.assertIn("About", driver.title)

class TestVirtualBookPublishing:
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
    py = r'C:\Users\84495\Desktop\VirtualBookPublishing\app.py'
    test = TestVirtualBookPublishing(checker, py)
    print(test.main())






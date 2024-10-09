import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select 
import time
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):
    def setUp(self):
        """Set up the Selenium WebDriver before each test."""
        self.driver = webdriver.Chrome()  # You can specify the path to your WebDriver here
        self.driver.get("http://localhost:5000")  # Start from the landing page
    
    def tearDown(self):
        """Tear down the WebDriver after each test."""
        self.driver.quit()
    
    def login(self):
        self.driver.delete_all_cookies()
        username = "user1"
        password = "pass123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

    def test_login_elements(self):
        """Test presence of critical elements on the Login Page."""
        self.driver.find_element(By.ID, "login-form")
        self.driver.find_element(By.ID, "username")
        self.driver.find_element(By.ID, "password")
        self.driver.find_element(By.ID, "login-button")
        self.driver.find_element(By.ID, "login-error")

    def test_login_functionality(self):
        """Test functionality of the Login Page."""
        self.assertEqual(self.driver.title, "User Login")

        username = 'user1'  # Example username
        password = 'pass123'  # Example password
        
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
        self.assertEqual(self.driver.title, "Expense Dashboard")

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register-button").click()
        self.assertEqual(self.driver.title, "User Register")
    
    def test_register_elements(self):
        """Test presence of critical elements on the register Page."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register-button").click()

        self.driver.find_element(By.ID, "register-form")
        self.driver.find_element(By.ID, "username")
        self.driver.find_element(By.ID, "password")
        self.driver.find_element(By.ID, "register-button")

    def test_register_functionality(self):
        """Test functionality of the register Page."""
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register-button").click()

        # Registering a new user
        username = "newuser"
        password = "newpassword"
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "register-button").click()
        
        # Check if redirected to Main Blog Page
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username}:{password}\n" in users)


    def test_dashboard_elements(self):
        """Test presence of critical elements on the Dashboard Page."""
        self.login()
        self.driver.find_element(By.ID, "dashboard-header")
        self.driver.find_element(By.ID, "expense-summary")
        self.driver.find_element(By.ID, "add-expense-button")
        self.driver.find_element(By.ID, "view-expense-button")
        self.driver.find_element(By.ID, "add-income-button")
        self.driver.find_element(By.ID, "report-button")
        self.driver.find_element(By.ID, "logout-button")

    def test_dashboard_functionality(self):
        """Test functionality of the Dashboard Page."""
        self.login()
        self.driver.find_element(By.ID, "add-expense-button").click()
        self.assertEqual(self.driver.title, "Add New Expense")

        self.login()
        self.driver.find_element(By.ID, "view-expense-button").click()
        self.assertEqual(self.driver.title, "View All Expenses")

        self.login()
        self.driver.find_element(By.ID, "add-income-button").click()
        self.assertEqual(self.driver.title, "Add New Income")

        self.login()
        self.driver.find_element(By.ID, "report-button").click()
        self.assertEqual(self.driver.title, "Expense Reports")

        self.login()
        self.driver.find_element(By.ID, "logout-button").click()
        self.assertEqual(self.driver.title, "User Login")

        self.login()
        expense_summary = self.driver.find_element(By.ID, "expense-summary").text
        with open(os.path.join('data', 'expenses.txt'), 'r') as file:
            expenses_ = file.readlines()
        expenses = [line.split('|')[2].strip() for line in expenses_]
        with open(os.path.join('data', 'income.txt'), 'r') as file:
            income_ = file.readlines()
        income = [line.split('|')[1].strip() for line in income_]
        total_expense = sum(expenses)
        total_income = sum(income)
        self.assertIn(total_expense, expense_summary)
        self.assertIn(total_income, expense_summary)


    def test_add_expense_elements(self):
        """Test presence of critical elements on the Add Expense Page."""
        self.login()
        self.driver.find_element(By.ID, "add-expense-button").click()  # Navigate to Add Expense Page
        
        self.driver.find_element(By.ID, "add-expense-form")
        self.driver.find_element(By.ID, "expense-name")
        self.driver.find_element(By.ID, "expense-amount")
        self.driver.find_element(By.ID, "expense-date")
        self.driver.find_element(By.ID, "submit-expense-button")

        dropdown_element = self.driver.find_element(By.ID, "expense-category")
        self.assertEqual(dropdown_element.tag_name, 'select')
        select = Select(dropdown_element)
        options = [option.text for option in select.options]
        expected_options = ['Clothing', 'Food', 'Housing', 'Transportation']
        self.assertEqual(options, expected_options)

    def test_add_expense_functionality(self):
        """Test functionality of the Add Expense Page."""
        self.login()  
        self.driver.find_element(By.ID, "add-expense-button").click()  # Ensure we're on the Add Expense Page
        
        expense_name = "Utilities"
        expense_amount = "100.00"
        expense_date = "202309-10-05"
        expense_category = "Clothing"

        self.driver.find_element(By.ID, "expense-name").send_keys(expense_name)
        self.driver.find_element(By.ID, "expense-amount").send_keys(expense_amount)
        self.driver.find_element(By.ID, "expense-date").send_keys(expense_date)
        select = Select(self.driver.find_element(By.ID, "expense-category"))
        select.select_by_visible_text(expense_category)
        self.driver.find_element(By.ID, "submit-expense-button").click()
        with open(os.path.join('data', 'expenses.txt'), 'r') as file:
            expenses_ = file.readlines()
        expenses_name = [line.split('|')[1].strip() for line in expenses_]
        self.assertIn(expense_name, expenses_name)

        self.login()
        # Verify that the expense was added by checking the expense list
        self.driver.find_element(By.ID, "view-expense-button").click()  # Navigate to the View Expenses Page
        expense_list = self.driver.find_element(By.ID, "expense-list").text
        self.assertIn(expense_name, expense_list)  # Check that the added expense appears in the list

    def test_add_income_elements(self):
        """Test presence of critical elements on the Add Expense Page."""
        self.login()
        self.driver.find_element(By.ID, "add-income-button").click()  # Navigate to Add Income Page
        
        self.driver.find_element(By.ID, "add-income-form")
        self.driver.find_element(By.ID, "income-amount")
        self.driver.find_element(By.ID, "income-date")
        self.driver.find_element(By.ID, "submit-income-button")

        dropdown_element = self.driver.find_element(By.ID, "income-category")
        self.assertEqual(dropdown_element.tag_name, 'select')
        select = Select(dropdown_element)
        options = [option.text for option in select.options]
        expected_options = ['Salary', 'Other']
        self.assertEqual(options, expected_options)    

    def test_add_income_functionality(self):
        """Test functionality of the Add Expense Page."""
        self.login()
        self.driver.find_element(By.ID, "add-income-button").click()  # Navigate to Add Expense Page
        
        income_amount = "100.00"
        income_date = "202309-10-05"
        income_category = "Other"

        self.driver.find_element(By.ID, "income-amount").send_keys(income_amount)
        self.driver.find_element(By.ID, "income-date").send_keys(income_date)
        select = Select(self.driver.find_element(By.ID, "income-category"))
        select.select_by_visible_text(income_category)
        self.driver.find_element(By.ID, "submit-income-button").click()
        with open(os.path.join('data', 'income.txt'), 'r') as file:
            income_ = file.readlines()
        self.assertIn(f"{income_date}|{income_amount}|{income_category}", income_)


    def test_view_expenses_elements(self):
        """Test presence of critical elements on the View Expenses Page."""
        self.login()
        self.driver.find_element(By.ID, "view-expense-button").click()  # Navigate to View Expenses Page
        
        self.driver.find_element(By.ID, "expense-list")
        self.driver.find_element(By.ID, "delete-expense-button")  # Assuming only the visibility check for first expense item

    def test_view_expenses_functionality(self):
        """Test functionality of the View Expenses Page."""
        self.login()
        self.driver.find_element(By.ID, "view-expense-button").click()  # Navigate to View Expenses Page
        expense_list = self.driver.find_element(By.ID, "expense-list").text
        with open(os.path.join('data', 'expenses.txt'), 'r') as file:
            expenses_ = file.readlines()
        expenses_name = [line.split('|')[1].strip() for line in expenses_]
        for item in expenses_name:
            self.assertIn(item, expense_list)
            
        self.driver.find_element(By.ID, "delete-expense-button").click()
        with open(os.path.join('data', 'expenses.txt'), 'r') as file:
            expenses_ = file.readlines()
        expenses_after_delete = [line.split('|')[1].strip() for line in expenses_]
        self.assertEqual(1, len(expenses_name)-len(expenses_after_delete))

    def test_reports_elements(self):
        """Test presence of critical elements on the Reports Page."""
        self.login()  # Ensure we've interacted with View Expenses
        self.driver.find_element(By.ID, "report-button").click() 
        
        self.driver.find_element(By.ID, "report-select")
        self.driver.find_element(By.ID, "generate-report-button")
        self.driver.find_element(By.ID, "report-output")

    def test_reports_functionality(self):
        """Test functionality of the Reports Page."""
        self.login()  # Ensure we've interacted with View Expenses
        self.driver.find_element(By.ID, "report-button").click() 

        # Trigger a report generation
        self.driver.find_element(By.ID, "report-select").send_keys("Monthly")
        self.driver.find_element(By.ID, "generate-report-button").click()

        # Verify that a report was generated
        report_output = self.driver.find_element(By.ID, "report-output").text
        self.assertTrue(len(report_output) > 0)  # Ensure there is some output


        self.login()  # Ensure we've interacted with View Expenses
        self.driver.find_element(By.ID, "report-button").click() 

        # Trigger a report generation
        self.driver.find_element(By.ID, "report-select").send_keys("Yearly")
        self.driver.find_element(By.ID, "generate-report-button").click()
        
        # Verify that a report was generated
        report_output = self.driver.find_element(By.ID, "report-output").text
        self.assertTrue(len(report_output) > 0)  # Ensure there is some output


class TestExpenseTracker:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\gpt-4o-mini-0\ExpenseTracker\app.py'
    test = TestExpenseTracker(checker, py)
    print(test.main())
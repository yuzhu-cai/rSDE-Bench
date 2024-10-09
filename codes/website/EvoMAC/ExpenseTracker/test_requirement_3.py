'''
Test cases for verifying the presence of required elements on each page of the ExpenseTracker application.
'''
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.username = "user1"  # Example username from users.txt
        self.password = "pass123"  # Example password from users.txt
    def login(self):
        driver = self.driver
        driver.find_element(By.ID, "username").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Wait for the dashboard to load
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "login-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "username").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "login-error").is_displayed())
    def test_register_page_elements(self):
        driver = self.driver
        driver.find_element(By.ID, "register-button").click()
        time.sleep(2)  # Wait for the register page to load
        self.assertTrue(driver.find_element(By.ID, "register-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "username").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "password").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "register-button").is_displayed())
    def test_dashboard_page_elements(self):
        self.login()
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, "dashboard-header").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "expense-summary").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "add-expense-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "view-expense-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "add-income-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "report-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "logout-button").is_displayed())
    def test_add_expense_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "add-expense-button").click()
        time.sleep(2)  # Wait for the add expense page to load
        self.assertTrue(driver.find_element(By.ID, "add-expense-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "expense-name").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "expense-amount").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "expense-date").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "expense-category").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit-expense-button").is_displayed())
    def test_add_income_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "add-income-button").click()
        time.sleep(2)  # Wait for the add income page to load
        self.assertTrue(driver.find_element(By.ID, "add-income-form").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "income-amount").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "income-date").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "income-category").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "submit-income-button").is_displayed())
    def test_view_expenses_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "view-expense-button").click()
        time.sleep(2)  # Wait for the view expenses page to load
        self.assertTrue(driver.find_element(By.ID, "expense-list").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "delete-expense-button").is_displayed())
    def test_reports_page_elements(self):
        self.login()
        driver = self.driver
        driver.find_element(By.ID, "report-button").click()
        time.sleep(2)  # Wait for the reports page to load
        self.assertTrue(driver.find_element(By.ID, "report-select").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "generate-report-button").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "report-output").is_displayed())
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()
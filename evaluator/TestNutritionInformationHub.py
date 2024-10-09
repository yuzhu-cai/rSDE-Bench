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
        # Initialize the webdriver and navigate to the landing page
        self.driver = webdriver.Chrome()  # Replace with the appropriate webdriver for your browser
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        # Close the webdriver session
        self.driver.quit()

    # Test functions for the Login Page
    def test_login_page_elements(self):
        driver = self.driver
        self.assertTrue(driver.find_element(By.ID, 'usernameField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'passwordField').is_displayed())
        self.assertTrue(driver.find_element(By.ID, 'loginButton').is_displayed())

    def test_login_page_functionality(self):
        driver = self.driver
        username = 'username1'  # Assume this is a valid user
        password = 'password1'  # Assume this is a valid password

        # Enter credentials and click login
        driver.find_element(By.ID, 'usernameField').send_keys(username)
        driver.find_element(By.ID, 'passwordField').send_keys(password)
        driver.find_element(By.ID, 'loginButton').click()

        # Check if redirected to Home Page by verifying an element's presence
        self.assertIn("Home", driver.title)

    # Test functions for the Home Page
    def test_home_page_elements(self):
        driver = self.driver
        self._navigate_to_home_page()
        driver.find_element(By.ID, 'nutritionInfoLink')
        driver.find_element(By.ID, 'recipeTrackerLink')
        driver.find_element(By.ID, 'logoutButton')

    def test_home_page_functionality(self):
        driver = self.driver
        self._navigate_to_home_page()
        
        # Verify logout functionality
        driver.find_element(By.ID, 'logoutButton').click()
        self.assertIn("User Login", driver.title)  # Should see login fields again
        username = 'username1'  # Assume this is a valid user
        password = 'password1'  # Assume this is a valid password

        # Enter credentials and click login
        driver.find_element(By.ID, 'usernameField').send_keys(username)
        driver.find_element(By.ID, 'passwordField').send_keys(password)
        driver.find_element(By.ID, 'loginButton').click()
        self.assertIn("Home", driver.title)  # Should be back on Home Page
        driver.find_element(By.ID, 'nutritionInfoLink').click()
        self.assertIn("Nutrition Information", driver.title)  # Should be back on Home Page
    # Test functions for the Nutrition Information Page
    def test_nutrition_info_page_elements(self):
        driver = self.driver
        self._navigate_to_nutrition_info_page()
        driver.find_element(By.ID, 'nutritionInfoTitle')
        driver.find_element(By.ID, 'searchField')
        driver.find_element(By.ID, 'searchButton')
        driver.find_element(By.ID, 'foodList')

    def test_nutrition_info_page_functionality(self):
        driver = self.driver
        self._navigate_to_nutrition_info_page()
        
        # Search for a food item
        search_item = 'apple'
        driver.find_element(By.ID, 'searchField').send_keys(search_item)
        driver.find_element(By.ID, 'searchButton').click()
        
        # Verify the expected result is displayed
        expected_result = 'apple'  # You would normally read from nutrition_info.txt
        food_list = driver.find_element(By.ID, 'foodList').text
        self.assertIn(expected_result, food_list)

    # Test functions for the Recipe Tracker Page
    def test_recipe_tracker_page_elements(self):
        driver = self.driver
        self._navigate_to_recipe_tracker_page()
        driver.find_element(By.ID, 'recipeTrackerTitle')
        driver.find_element(By.ID, 'recipeNameField')
        driver.find_element(By.ID, 'ingredientsField')
        driver.find_element(By.ID, 'instructionsField')
        driver.find_element(By.ID, 'saveRecipeButton')
        driver.find_element(By.ID, 'savedRecipesList')

    def test_recipe_tracker_page_functionality(self):
        driver = self.driver
        self._navigate_to_recipe_tracker_page()
        
        # Input a new recipe
        recipe_name = 'pizza'
        ingredients = 'cheese, milk, eggs'
        instructions = 'Mix ingredients, cook in oven'
        
        driver.find_element(By.ID, 'recipeNameField').send_keys(recipe_name)
        driver.find_element(By.ID, 'ingredientsField').send_keys(ingredients)
        driver.find_element(By.ID, 'instructionsField').send_keys(instructions)
        driver.find_element(By.ID, 'saveRecipeButton').click()
        
        # Verify the saved recipe is displayed
        saved_recipes = driver.find_element(By.ID, 'savedRecipesList').text
        self.assertIn(recipe_name, saved_recipes)
        with open(os.path.join('data', 'recipes.txt'), 'r') as file:
            users = file.readlines()
        exists = any("pizza|cheese, milk, eggs|Mix ingredients, cook in oven" in line for line in users)
        self.assertTrue(exists)
    def _navigate_to_home_page(self):
        self.driver.find_element(By.ID, 'usernameField').send_keys('username1')
        self.driver.find_element(By.ID, 'passwordField').send_keys('password1')
        self.driver.find_element(By.ID, 'loginButton').click()  # Assume already logged in

    def _navigate_to_nutrition_info_page(self):
        self._navigate_to_home_page()
        self.driver.find_element(By.ID, 'nutritionInfoLink').click()

    def _navigate_to_recipe_tracker_page(self):
        self._navigate_to_home_page()
        self.driver.find_element(By.ID, 'recipeTrackerLink').click()



class TestNutritionInformationHub:
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
            'total': 9,
            'total_basic': 5,
            'total_advanced': 4,
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
    py = r'D:\research\asie-bench_withweb\codes\gpt-4o-mini-0\NutritionInformationHub\app.py'
    test = TestNutritionInformationHub(checker, py)
    print(test.main())





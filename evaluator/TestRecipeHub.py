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
        password = "password123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_elements(self):
        """Test presence and accessibility of critical elements on the login page."""
        self.driver.find_element(By.ID, "username_input")
        self.driver.find_element(By.ID, "password_input")
        self.driver.find_element(By.ID, "login_button")
        self.driver.find_element(By.ID, "register_button")
        #self.driver.find_element(By.ID, "error_message")

    def test_login_functionality(self):
        """Test login functionality with valid credentials."""
        self.assertEqual(self.driver.title, "Login")

        self.driver.find_element(By.ID, "username_input").send_keys("user1")
        self.driver.find_element(By.ID, "password_input").send_keys("password123")
        self.driver.find_element(By.ID, "login_button").click()
        self.assertIn("Home", self.driver.title)  # Example expected title
        
        self.driver.back()
        self.driver.find_element(By.ID, "register_button").click()
        self.assertEqual(self.driver.title, "Register")

    # Registration Page Tests
    def test_registration_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()
        self.driver.find_element(By.ID, 'username_input')
        self.driver.find_element(By.ID, 'password_input')
        self.driver.find_element(By.ID, 'register_button')
        #self.driver.find_element(By.ID, 'error_message')

    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "register_button").click()
        username = "newusername"
        password = "newpassword"
        self.driver.find_element(By.ID, 'username_input').send_keys(username)
        self.driver.find_element(By.ID, 'password_input').send_keys(password)
        self.driver.find_element(By.ID, 'register_button').click()
        
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
        self.assertTrue(f"{username}:{password}\n" in users)

    # Home Page Tests
    def test_home_elements(self):
        """Test presence and accessibility of critical elements on the home page."""
        # Navigate to Home
        self.login()
        self.driver.find_element(By.ID, "welcome_message")
        self.driver.find_element(By.ID, "view_recipes_button")
        self.driver.find_element(By.ID, "submit_recipe_button")
        self.driver.find_element(By.ID, "profile_button")
        self.driver.find_element(By.ID, "logout_button")

    def test_home_functionality(self):
        """Test functionality of buttons on the home page."""
        self.login()
        welcom_text = self.driver.find_element(By.ID, "welcome_message").text
        self.assertIn('welcom', welcom_text.lower())

        # Check button functionalities by navigating
        self.driver.find_element(By.ID, "submit_recipe_button").click()
        self.assertIn("Submit Recipe", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "view_recipes_button").click()
        self.assertIn("Browse Recipes", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "profile_button").click()
        self.assertIn("User Profile", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "logout_button").click()
        self.assertIn("Login", self.driver.title)

    # Submit Recipe Page Tests
    def test_recipe_submission_elements(self):
        """Test presence and accessibility of critical elements on the recipe submission page."""
        self.login()
        self.driver.find_element(By.ID, "submit_recipe_button").click()

        self.driver.find_element(By.ID, "recipe_title_input")
        self.driver.find_element(By.ID, "ingredients_input")
        self.driver.find_element(By.ID, "instructions_input")
        self.driver.find_element(By.ID, "submit_recipe_button")
        #self.driver.find_element(By.ID, "submission_success_message")
        #self.driver.find_element(By.ID, "submission_error_message")

    def test_recipe_submission_functionality(self):
        """Test recipe submission functionality."""
        self.login()
        self.driver.find_element(By.ID, "submit_recipe_button").click()

        recipe_title = "Test Recipe"
        recipe_ingredients = "ingredient1, ingredient2"
        recipe_instructions = "Do this and that"
        
        self.driver.find_element(By.ID, "recipe_title_input").send_keys(recipe_title)
        self.driver.find_element(By.ID, "ingredients_input").send_keys(recipe_ingredients)
        self.driver.find_element(By.ID, "instructions_input").send_keys(recipe_instructions)
        self.driver.find_element(By.ID, "submit_recipe_button").click()

        success_message = self.driver.find_element(By.ID, "submission_success_message").text
        self.assertIn("success", success_message.lower())

        with open(os.path.join('data', 'recipes.txt'), 'r') as file:
            recipes = file.readlines()
        self.assertIn(f"2;{recipe_title};{recipe_ingredients};{recipe_instructions}\n", recipes)

    # Browse Recipes Page Tests
    def test_browsing_elements(self):
        """Test presence and accessibility of critical elements on the browsing page."""
        self.login()
        self.driver.find_element(By.ID, "view_recipes_button").click()
        self.driver.find_element(By.ID, "search_input")
        self.driver.find_element(By.ID, "search_button")
        self.driver.find_element(By.ID, "search_result")
        self.driver.find_element(By.ID, "recipe_list")
        self.driver.find_element(By.ID, "back_to_home_button")
        self.driver.find_element(By.ID, "recipe_details_button_1")

    def test_browsing_functionality(self):
        """Test that searching and selecting a recipe works correctly."""
        self.login()
        self.driver.find_element(By.ID, "view_recipes_button").click()
        self.driver.find_element(By.ID, "back_to_home_button").click()
        self.assertIn("Home", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "view_recipes_button").click()
        self.driver.find_element(By.ID, "search_input").send_keys("Pancakes")
        self.driver.find_element(By.ID, "search_button").click()

        search_result = self.driver.find_element(By.ID, "search_result").text
        with open(os.path.join('data', 'recipes.txt'), 'r') as file:
            recipes = file.readlines()
        recipe_pancakes = [].extend(recipe.split(";")[1:] for recipe in recipes if "Pancakes" in recipe)
        for item in recipe_pancakes:
            self.assertIn(item, search_result)
        
        self.driver.find_element(By.ID, "recipe_details_button_0").click()
        self.assertIn("Recipe Details", self.driver.title)
    
    
    def test_profile_elements(self):
        """Test presence and accessibility of critical elements on the user profile page."""
        self.login()
        self.driver.find_element(By.ID, "profile_button").click()
        
        self.driver.find_element(By.ID, "username_display")
        self.driver.find_element(By.ID, "user_recipes_list")
        self.driver.find_element(By.ID, "delete_account_button")

    def test_profile_functionality(self):
        """Test the edit profile button functionality."""
        self.driver.delete_all_cookies()
        username = "user2"
        password = "mySecurePassword"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_input").send_keys(username)
        self.driver.find_element(By.ID, "password_input").send_keys(password)
        self.driver.find_element(By.ID, "login_button").click()
        self.driver.find_element(By.ID, "profile_button").click()
        
        self.driver.find_element(By.ID, "delete_account_button").click()
        self.assertIn("Login", self.driver.title)

        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
        print("users: ", users)
        self.assertTrue(f"{username}:{password}\n" not in users)
    
    def test_recipe_details_elements(self):
        """Test presence and accessibility of critical elements on the recipe details page."""
        self.login()
        self.driver.find_element(By.ID, "view_recipes_button").click()
        self.driver.find_element(By.ID, "recipe_details_button_1").click()
        
        self.driver.find_element(By.ID, "recipe_title")
        self.driver.find_element(By.ID, "recipe_ingredient")
        self.driver.find_element(By.ID, "recipe_instruction")
        self.driver.find_element(By.ID, "back_to_home_button")
    
    def test_recipe_details_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "view_recipes_button").click()
        self.driver.find_element(By.ID, "recipe_details_button_1").click()
        self.driver.find_element(By.ID, "back_to_home_button").click()
        self.assertIn("Home", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "view_recipes_button").click()
        self.driver.find_element(By.ID, "recipe_details_button_1").click()

        title = self.driver.find_element(By.ID, "recipe_title").text
        ingredient = self.driver.find_element(By.ID, "recipe_ingredient").text
        instruction = self.driver.find_element(By.ID, "recipe_instruction").text

        self.assertIn(title, 'Spaghetti;')
        self.assertIn(ingredient, 'spaghetti,tomato sauce;')
        self.assertIn(instruction, 'Boil spaghetti;Serve with sauce')

class TestRecipeHub:
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-1\RecipeHub\app.py'
    test = TestRecipeHub(checker, py)
    print(test.main())
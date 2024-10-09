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
        # Initialize WebDriver (make sure the correct driver is installed and in PATH)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        self.driver.quit()

    def login(self):
        self.driver.delete_all_cookies()
        username = "user1"
        password = "secret123"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "usernameField").send_keys(username)
        self.driver.find_element(By.ID, "passwordField").send_keys(password)
        self.driver.find_element(By.ID, "loginButton").click()

    # Login Page Tests
    def test_login_elements(self):
        self.assertEqual(self.driver.title, "User Login")

        self.driver.find_element(By.ID, "loginForm")
        self.driver.find_element(By.ID, "usernameField")
        self.driver.find_element(By.ID, "passwordField")
        self.driver.find_element(By.ID, "loginButton")
        self.driver.find_element(By.ID, "errorMessage")
        self.driver.find_element(By.ID, "registerLink")
    
    def test_login_functionality(self):
        self.driver.find_element(By.ID, "usernameField").send_keys("user1")
        self.driver.find_element(By.ID, "passwordField").send_keys("secret123")
        self.driver.find_element(By.ID, "loginButton").click()

        # Check if redirected to the home page
        self.assertEqual(self.driver.title, "Movie Recommendations")

        # Check if redirected to the User Registration Page by checking the title
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "registerLink").click()
        self.assertEqual(self.driver.title, "User Register")

    
    # Registration Page Tests
    def test_registration_elements(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "registerLink").click()

        self.driver.find_element(By.ID, "registerForm")
        self.driver.find_element(By.ID, "usernameField")
        self.driver.find_element(By.ID, "passwordField")
        self.driver.find_element(By.ID, "registerButton")
        self.driver.find_element(By.ID, "errorMessage")

    def test_registration_functionality(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "registerLink").click()

        # Registering a new user
        username = "newuser"
        password = "newpassword"

        self.driver.find_element(By.ID, "usernameField").send_keys(username)
        self.driver.find_element(By.ID, "passwordField").send_keys(password)
        self.driver.find_element(By.ID, "registerButton").click()

        # Check if redirected to Main Blog Page
        with open(os.path.join('data', 'users.txt'), 'r') as f:
            users = f.readlines()
            self.assertTrue(f"{username},{password}\n" in users)
    
    # Home Page Tests
    def test_home_elements(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "welcomeMessage")
        self.driver.find_element(By.ID, "searchButton")
        self.driver.find_element(By.ID, "favoriteButton")
        self.driver.find_element(By.ID, "recommendationsList")
        self.driver.find_element(By.ID, "viewDetailsButton_1")
    
    def test_home_functionality(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "searchButton").click()
        self.assertEqual(self.driver.title, "Search Movies")

        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "favoriteButton").click()
        self.assertEqual(self.driver.title, "Favorite Movies")

        self.login()  # Ensure we're logged in
        recommendationsList = self.driver.find_element(By.ID, "recommendationsList").text
        with open(os.path.join('data', 'movies.txt'), 'r') as file:
            movies = file.readlines()
        movies_list = [line.split(',')[1].strip() for line in movies]
        for movie in movies_list:
            self.assertIn(movie, recommendationsList)

        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "viewDetailsButton_1").click()
        self.assertEqual(self.driver.title, "Movie Details")

    # Search Page Tests
    def test_search_elements(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "searchButton").click()

        self.driver.find_element(By.ID, "searchField")
        self.driver.find_element(By.ID, "searchButton")
        #self.driver.find_element(By.ID, "searchResult")

    def test_search_functionality(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "searchButton").click()

        self.driver.find_element(By.ID, "searchField").send_keys("Inception")
        self.driver.find_element(By.ID, "searchButton").click()

        result = self.driver.find_element(By.ID, "searchResult").text

        self.assertIn('Inception', result)

    # Movie Details Page Tests
    def test_movie_details_elements(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "viewDetailsButton_1").click()
        self.driver.find_element(By.ID, "movieTitle")
        self.driver.find_element(By.ID, "movieDescription")
        self.driver.find_element(By.ID, "movieRating")
        self.driver.find_element(By.ID, "addToFavoritesButton")
        self.driver.find_element(By.ID, "backToHomeButton")

    def test_movie_details_functionality(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "viewDetailsButton_1").click()
        self.driver.find_element(By.ID, "addToFavoritesButton").click()

        # Verify if it was added to favorites
        with open(os.path.join('data', 'favorites.txt'), 'r') as file:
            favorites = file.readlines()
        favorites_list = [line.split(',')[1].strip() for line in favorites if line.startswith("user1")]
        self.assertIn("1", favorites_list)

        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "viewDetailsButton_1").click()
        self.driver.find_element(By.ID, "backToHomeButton").click()
        self.assertEqual(self.driver.title, "Movie Recommendations")


    # Favorites Page Tests
    def test_favorites_elements(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "favoriteButton").click()
        print(self.driver.page_source)
        self.driver.find_element(By.ID, "favoriteViewDetailsButton_2")
        self.driver.find_element(By.ID, "removeFromFavoritesButton_2")
    
    def test_favorites_functionality(self):
        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "favoriteButton").click()
        self.driver.find_element(By.ID, "favoriteViewDetailsButton_2").click()
        # Check if redirected to the movie details page
        self.assertEqual(self.driver.title, "Movie Details")

        self.login()  # Ensure we're logged in
        self.driver.find_element(By.ID, "favoriteButton").click()
        self.driver.find_element(By.ID, "removeFromFavoritesButton_2").click()
        with open(os.path.join('data', 'favorites.txt'), 'r') as file:
            favorites = file.readlines()
        favorites_list = [line.split(',')[1].strip() for line in favorites if line.startswith("user1")]
        self.assertNotIn("2", favorites_list)


class TestMovieRecommendationSystem:
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
    py = r'D:\research\asie-bench-yuzhucai-final\codes\gpt-4o-mini-0\MovieRecommendationSystem\app.py'
    test = TestMovieRecommendationSystem(checker, py)
    print(test.main())
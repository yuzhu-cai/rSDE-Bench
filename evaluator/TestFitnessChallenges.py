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
        username = "johnsmith"
        password = "password123"
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "usernameField").send_keys(username)
        self.driver.find_element(By.ID, "passwordField").send_keys(password)
        self.driver.find_element(By.ID, "loginButton").click()
    
    # Page 1: Login Page Tests
    def test_login_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "loginForm").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "usernameField").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "passwordField").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "loginButton").is_displayed())

    def test_login_page_functionality(self):
        # Assuming a valid user exists in users.txt
        self.assertIn("User Login", self.driver.title)
        username = "johnsmith"
        password = "password123"

        self.driver.find_element(By.ID, "usernameField").send_keys(username)
        self.driver.find_element(By.ID, "passwordField").send_keys(password)
        self.driver.find_element(By.ID, "loginButton").click()
        self.assertIn("User Dashboard", self.driver.title)


    # Page 2: Dashboard Tests
    def test_dashboard_elements(self):
        self.login()
        
        self.assertTrue(self.driver.find_element(By.ID, "userProfile").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "currentChallenges").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "activityLog").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "startChallengeButton").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "logoutButton").is_displayed())

    def test_dashboard_functionality(self):
        self.login()
        profile = self.driver.find_element(By.ID, "userProfile").text
        self.assertIn("johnsmith", profile)

        currentChallenges = self.driver.find_element(By.ID, "currentChallenges").text
        self.assertIn("30-Day Yoga Challenge", currentChallenges)

        activityLog = self.driver.find_element(By.ID, "activityLog").text
        self.assertIn("Joined '30-Day Yoga Challenge'", activityLog)
        self.assertNotIn("Updated progress for '10K Run Challenge", activityLog)

        # Simulate starting a new challenge
        self.driver.find_element(By.ID, "startChallengeButton").click()
        self.assertIn("Challenges", self.driver.title)

        self.login()
        self.driver.find_element(By.ID, "logoutButton").click()
        self.assertIn("User Login", self.driver.title)

    # Page 3: Challenges List Tests
    def test_challenges_list_elements(self):
        self.login()
        self.driver.find_element(By.ID, "startChallengeButton").click()

        self.assertTrue(self.driver.find_element(By.ID, "challengesTable").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "progressButton").is_displayed())

    def test_challenges_list_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "startChallengeButton").click()
        
        challengeTable = self.driver.find_element(By.ID, "challengesTable").text
        with open('data/challenges.txt', 'r') as file:
            challengs = file.readlines()
        challengeName = [line.split(":")[0].strip() for line in challengs]
        challengeDescription = [line.split(":")[1].strip() for line in challengs]
        challengeDuration = [line.split(":")[2].strip() for line in challengs]
        for item in challengeName:
            self.assertIn(item, challengeTable)
        for item in challengeDescription:
            self.assertIn(item, challengeTable)
        for item in challengeDuration:
            self.assertIn(item, challengeTable)

        self.driver.find_element(By.ID, "progressButton").click()
        self.assertIn("Progress Tracker", self.driver.title)

    # Page 4: Progress Tracker Tests
    def test_progress_tracker_elements(self):
        self.login()
        self.driver.find_element(By.ID, "startChallengeButton").click()
        self.driver.find_element(By.ID, "progressButton").click()

        self.assertTrue(self.driver.find_element(By.ID, "challengeName").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "currentProgress").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "updateProgressButton").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "addNotesField").is_displayed())

    def test_progress_tracker_functionality(self):
        self.login()
        self.driver.find_element(By.ID, "startChallengeButton").click()
        self.driver.find_element(By.ID, "progressButton").click()

        progress_input = self.driver.find_element(By.ID, "currentProgress")
        notes_input = self.driver.find_element(By.ID, "addNotesField")
        update_progress_button = self.driver.find_element(By.ID, "updateProgressButton")

        challengeName = self.driver.find_element(By.ID, "challengeName").text
        with open('data/current_challenges.txt', 'r') as file:
            current_challengs = file.readlines()
        current_challeng_names = [line.split(":")[1].strip() for line in current_challengs if line.split(":")[0] == "johnsmith"]
        for name in current_challeng_names:
            self.assertIn(name, challengeName)

        # Update progress
        previous_progress = progress_input.get_attribute("value")
        previous_notes = notes_input.get_attribute("value")
        
        with open('data/progress.txt', 'r') as file:
            progress = file.readlines()
        currentProgress = [line.split(":")[2] for line in progress if line.split(":")[0] == "johnsmith"]
        notes = [line.split(":")[3] for line in progress if line.split(":")[0] == "johnsmith"]
        self.assertIn(previous_progress, " ".join(currentProgress))
        self.assertIn(previous_notes, " ".join(notes))

        progress_input.clear()
        progress_input.send_keys("20 days")
        notes_input.clear()
        notes_input.send_keys("Still going strong!")
        update_progress_button.click()
        with open('data/progress.txt', 'r') as file:
            progress = file.readlines()
        currentProgress = [line.split(":")[2] for line in progress if line.split(":")[0] == "johnsmith"]
        notes = [line.split(":")[3] for line in progress if line.split(":")[0] == "johnsmith"]
        self.assertIn("20 days", " ".join(currentProgress))
        self.assertIn("Still going strong!", " ".join(notes))


class TestFitnessChallenges:
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
    py = r'D:\Dev\workspace\VSCodeSpace\Python\test\asie-bench-yhu\codes\WareHouse\FitnessChallenges\app.py'
    test = TestFitnessChallenges(checker, py)
    print(test.main())
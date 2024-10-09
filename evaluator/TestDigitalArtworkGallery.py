import os
import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

sys.path.append(os.path.abspath('evaluator')) 
from custom_test import CustomTestRunner
from utils_win import get_python_pid

class TestCase(unittest.TestCase):

    def setUp(self):
        # Initialize the web driver (make sure to provide the proper path for your web driver)
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        # Close the browser session
        self.driver.quit()
    
    def login(self):
        self.driver.delete_all_cookies()
        username = "john_doe"
        password = "abcd1234"
        
        # Performing login
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.ID, "username_field").send_keys(username)
        self.driver.find_element(By.ID, "password_field").send_keys(password)
        time.sleep(1)
        self.driver.find_element(By.ID, "login_button").click()

    # Login Page Tests
    def test_login_elements(self):
        self.assertEqual(self.driver.title, "Login")
        self.driver.find_element(By.ID, "username_field")
        self.driver.find_element(By.ID, "password_field")
        self.driver.find_element(By.ID, "login_button")
        self.driver.find_element(By.ID, "error_message")

    def test_login_functionality(self):
        self.driver.find_element(By.ID, "username_field").send_keys("john_doe")
        self.driver.find_element(By.ID, "password_field").send_keys("abcd1234")
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "login_button").click()
        self.assertIn("Gallery", self.driver.title)

    # Gallery Page Tests
    def test_gallery_elements(self):
        self.login()
        self.assertIn("Gallery", self.driver.title)
        self.driver.find_element(By.ID, "artwork_grid")
        # self.driver.find_element(By.ID, "artwork_title_field")
        self.driver.find_element(By.ID, "view_artwork_button")
        self.driver.find_element(By.ID, "delete_artwork_button")
        self.driver.find_element(By.ID, "upload_artwork_button")

    def test_gallery_functionality(self):
        self.login()

        # Test the Upload Artwork functionality
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "upload_artwork_button").click()
        self.assertEqual(self.driver.title, "Upload Artwork")

        # Test the View Artwork functionality
        self.login()
        # self.driver.find_element(By.ID, "artwork_title_field").send_keys("Sunset Over the Hills")
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "view_artwork_button").click()
        self.assertIn("View Artwork", self.driver.title)

        # Test the Delete Artwork functionality
        self.login()
        # self.driver.find_element(By.ID, "artwork_title_field").send_keys("Sunset Over the Hills")
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "delete_artwork_button").click()
        with open(os.path.join('data', 'artworks.txt'), 'r') as file:
            artworks = file.readlines()
        titles = [line.split('|')[1].strip() for line in artworks]
        self.assertNotIn("Sunset Over the Hills", titles)

    # Upload Artwork Page Tests
    def test_upload_artwork_elements(self):
        self.login()
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "upload_artwork_button").click()
        self.assertEqual(self.driver.title, "Upload Artwork")
        self.driver.find_element(By.ID, "artwork_title_field")
        self.driver.find_element(By.ID, "artwork_description_field")
        # self.driver.find_element(By.ID, "artwork_file_field")
        self.driver.find_element(By.ID, "upload_button")
        self.driver.find_element(By.ID, "cancel_button")

    def test_upload_artwork_functionality(self):
        self.login()
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "upload_artwork_button").click()
        # Uploading artwork
        self.driver.find_element(By.ID, "artwork_title_field").send_keys("Test Artwork")
        self.driver.find_element(By.ID, "artwork_description_field").send_keys("Test description.")
        # current_directory = os.getcwd()
        # self.driver.find_element(By.ID, "artwork_file_field").send_keys("Test Artwork")
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "upload_button").click()

        with open(os.path.join('data', 'artworks.txt'), 'r') as file:
            artworks = file.readlines()
        titles = [line.split('|')[1].strip() for line in artworks]
        print(titles)
        self.assertIn("Test Artwork", titles)
        

        # Testing cancel button
        self.login()
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "upload_artwork_button").click()
        # self.driver.find_element(By.ID, "artwork_title_field").send_keys("Cancel Artwork")
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "cancel_button").click()
        self.assertEqual(self.driver.title, "Gallery")

        with open(os.path.join('data', 'artworks.txt'), 'r') as file:
            artworks = file.readlines()
        titles = [line.split('|')[1].strip() for line in artworks]
        self.assertNotIn("Cancel Artwork", titles)

    # View Artwork Page Tests
    def test_view_artwork_elements(self):
        self.login()
        # self.driver.find_element(By.ID, "view_artwork_button").click()        
        # self.driver.find_element(By.ID, "artwork_title_field").send_keys("Abstract Shapes")
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "view_artwork_button").click()
        self.driver.find_element(By.CSS_SELECTOR, "h1")
        self.driver.find_element(By.CSS_SELECTOR, "p")
        # self.driver.find_element(By.ID, "full-size_artwork")
        self.driver.find_element(By.ID, "back_button")

    def test_view_artwork_functionality(self):
        self.login()
        # self.driver.find_element(By.ID, "view_artwork_button").click()                
        # self.driver.find_element(By.ID, "artwork_title_field").send_keys("Abstract Shapes")
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "view_artwork_button").click()
        self.assertIn("View Artwork", self.driver.title)
        # displayed_title = self.driver.find_element(By.ID, "full-size_artwork").get_attribute("alt")
        # displayed_source = self.driver.find_element(By.ID,  "full-size_artwork").get_attribute("src")
        # self.assertIn("Abstract Shapes", displayed_title)
        # self.assertTrue(displayed_source.endswith("abstract.png"))
        # time.sleep(self.time)
        self.driver.find_element(By.ID, "back_button").click()
        self.assertIn("Gallery", self.driver.title)

class TestDigitalArtworkGallery:
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
    py = r'C:\Users\84495\Desktop\asie-bench\codes\gpt-4o-mini-0\DigitalArtworkGallery\app.py'
    test = TestDigitalArtworkGallery(checker, py)
    print(test.main())

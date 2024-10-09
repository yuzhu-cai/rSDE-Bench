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
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        self.driver.quit()


    def test_login_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'password').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'login_button').is_displayed())

    def test_login_functionality(self):
        self.driver.find_element(By.ID, 'username').send_keys('user1')  # Assuming user1 with password 123 exists
        self.driver.find_element(By.ID, 'password').send_keys('123')
        self.driver.find_element(By.ID, 'login_button').click()
        time.sleep(1)  # Wait for potential page load
        self.assertIn("Festival List", self.driver.title)

    def test_festival_list_elements(self):
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('123')
        self.driver.find_element(By.ID, 'login_button').click()
        self.assertTrue(self.driver.find_element(By.ID, 'festival_list').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add_festival_page_button').is_displayed())

        festival_items = self.driver.find_elements(By.XPATH, "//*[starts-with(@id, 'festival_item_')]")
        self.assertGreater(len(festival_items), 0)

    def test_festival_list_functionality(self):
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('123')
        self.driver.find_element(By.ID, 'login_button').click()
        festivals_data = {}
        with open('./data/festivals.txt', 'r') as f:
            for line in f:
                name, location, date, lineup = line.strip().split('|')
                festivals_data[name] = (location, date, lineup)

        festival_items = self.driver.find_elements(By.XPATH, "//*[starts-with(@id, 'festival_item_')]")
        for index, item in enumerate(festival_items):
            item.click()
            time.sleep(1)
            self.assertIn("Festival Details", self.driver.title)
            break


    def test_festival_details_elements(self):
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('123')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, 'festival_item_1').click()
        self.assertTrue(self.driver.find_element(By.ID, 'festival_name').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'festival_location').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'festival_date').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'festival_lineup').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'back_to_list_button').is_displayed())

    def test_festival_details_functionality(self):
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('123')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, 'festival_item_1').click()
        self.driver.find_element(By.ID, 'back_to_list_button').click()
        self.assertIn("Festival List", self.driver.title)


            # festival_name = self.driver.find_element(By.ID, 'festival_name').text
            # self.assertIn(festival_name, festivals_data)
            # location, date, lineup = festivals_data[festival_name]
            # self.assertEqual(self.driver.find_element(By.ID, 'festival_location').text, location)
            # self.assertEqual(self.driver.find_element(By.ID, 'festival_date').text, date)
            # self.assertEqual(self.driver.find_element(By.ID, 'festival_lineup').text, lineup)
            # self.driver.find_element(By.ID, 'back_to_list_button').click()
            # time.sleep(1)

    def test_add_festival_elements(self):
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('123')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, 'add_festival_page_button').click()
        self.assertTrue(self.driver.find_element(By.ID, 'add_festival_name').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add_festival_location').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add_festival_date').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'add_festival_lineup').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'submit_button').is_displayed())


    def test_add_festival_functionality(self):
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('123')
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, 'add_festival_page_button').click()
        self.driver.find_element(By.ID, 'add_festival_name').send_keys('New Festival')
        self.driver.find_element(By.ID, 'add_festival_location').send_keys('New Location')
        self.driver.find_element(By.ID, 'add_festival_date').send_keys('202309-09-10')
        time.sleep(10)
        self.driver.find_element(By.ID, 'add_festival_lineup').send_keys('ArtistX, ArtistY')
        self.driver.find_element(By.ID, 'submit_button').click()
        time.sleep(1)


        # Validate by checking the festivals.txt file
        with open('./data/festivals.txt', 'r') as f:
            festivals = f.readlines()
            self.assertIn("New Festival|New Location|202309-09-10|ArtistX, ArtistY\n", festivals)


class TestMusicFestivalDirectory:
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
    py = r'D:\research\asie-bench_withweb\codes\gpt-4o-mini-0\MusicFestivalDirectory\app.py'
    test = TestMusicFestivalDirectory(checker, py)
    print(test.main())






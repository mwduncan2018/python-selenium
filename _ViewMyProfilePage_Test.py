import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestViewMyProfilePage(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(10)
        inst.driver.maximize_window()
        # create test users
        inst.gorilla = MikeBookUser("TestGorilla",
                               "Gorilla",
                               "testTwentySix",
                               "testTwentySix",
                               "I'm a test gorilla.",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               inst.driver)
        inst.gorilla.Register()

    def test_01_verify_that_user_info_displays_correctly(self):
        # verify that user info displays correctly
        # 1) Name
        # 2) Username
        # 3) About ME
        self.gorilla.Login()
        time.sleep(1)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkProfile'))).click()
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkViewMyProfile'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div[2]/div[1]/p'), self.gorilla.name))
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div[2]/div[2]/p'), self.gorilla.username))
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div[2]/div[3]/p'), self.gorilla.aboutMe))
        self.gorilla.Logout()
    
    @classmethod
    def tearDownClass(inst):
        # remove all test users
        inst.gorilla.Delete()
        # close browser
        inst.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)

    

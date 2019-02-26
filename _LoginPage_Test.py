import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestLoginPage(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(10)
        inst.driver.maximize_window()
        inst.driver.get("http://localhost/socialnetwork/login.php/")
        # create test users
        inst.gorilla = MikeBookUser("TestGorilla",
                               "Gorilla",
                               "testTwentySix",
                               "testTwentySix",
                               "I'm a test gorilla.",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               inst.driver)
        inst.bach = MikeBookUser("TestBach",
                            "BachLovin",
                            "testTwentySeven",
                            "testTwentySeven",
                            "I'm a test musician.",
                            "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestBach01.jpeg",
                            inst.driver)
        inst.rhino = MikeBookUser("TestRhino",
                             "RhinoLovin",
                             "testTwentyEight",
                             "testTwentyEight",
                             "I'm a test rhino.",
                             "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestRhino01.png",
                             inst.driver)
        inst.gorilla.Register()
        inst.bach.Register()
        inst.rhino.Register()
    
    def test_01_invalid_username_and_valid_password_combination_displays_error_message_and_user_is_not_logged_in_and_fields_maintain_values(self):
        # verify INVALID username and VALID password results in:
        # 1) ERROR MESSAGE
        # 2) NOT LOGGED IN
        # 3) Field maintain their values
        self.driver.get("http://localhost/socialnetwork/login.php/")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).send_keys('GeorgeTest')
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).send_keys(self.gorilla.password)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        # check an error message is displayed
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div/form/div[3]/span'), '* Username/Password combination is invalid'))
        # check that user is NOT logged in
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[1]/div/p'), 'Not logged in'))
        # check that fields maintain values
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).get_attribute('value'), 'GeorgeTest')
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).get_attribute('value'), self.gorilla.password)
    
    def test_02_valid_username_and_invalid_password_combination_displays_error_message_and_user_is_not_logged_in_and_fields_maintain_values(self):
        # verify VALID username and INVALID password results in:
        # 1) ERROR MESSAGE
        # 2) NOT LOGGED IN
        # 3) Field maintain their values
        self.driver.get("http://localhost/socialnetwork/login.php/")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).send_keys(self.gorilla.username)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).send_keys('JungleTest')
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        # check an error message is displayed
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div/form/div[3]/span'), '* Username/Password combination is invalid'))
        # check that user is NOT logged in
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[1]/div/p'), 'Not logged in'))
        # check that fields maintain values
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).get_attribute('value'), self.gorilla.username)
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).get_attribute('value'), 'JungleTest')
    
    def test_03_invalid_username_and_invalid_password_combination_displays_error_message_and_user_is_not_logged_in_and_fields_maintain_values(self):
        # verify INVALID username and INVALID password results in:
        # 1) ERROR MESSAGE
        # 2) NOT LOGGED IN
        # 3) Field maintain their values
        self.driver.get("http://localhost/socialnetwork/login.php/")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).send_keys('GeorgeTest')
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).send_keys('JungleTest')
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        # check an error message is displayed
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div/form/div[3]/span'), '* Username/Password combination is invalid'))
        # check that user is NOT logged in
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[1]/div/p'), 'Not logged in'))
        # check that fields maintain values
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).get_attribute('value'), 'GeorgeTest')
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).get_attribute('value'), 'JungleTest')

    def test_04_vaid_username_and_valid_password_combination_logs_user_in(self):
        # verify VALID username and VALID password results in:
        # 1) USER LOGGED IN
        # 2) Redirects to VIEW MY PROFILE page
        self.gorilla.Login()
        # check that user is logged in
        correct_text = 'Logged in as ' + self.gorilla.username
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[1]/div/p'), correct_text))
        # check redirected to VIEW MY PROFILE page
        self.assertEqual(self.driver.current_url, 'http://localhost/socialnetwork/viewmyprofile.php/')  
        self.gorilla.Logout()
    
    @classmethod
    def tearDownClass(inst):
        # remove all test users
        inst.gorilla.Delete()
        inst.bach.Delete()
        inst.rhino.Delete()
        # close browser
        inst.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)

    

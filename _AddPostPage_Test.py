import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestAddPostPage(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(10)
        inst.driver.maximize_window()
        # create test users
        inst.gorilla = MikeBookUser("TestGorilla",
                                    "Gorilla",
                                    "testThirtyFive",
                                    "testThirtyFive",
                                    "I'm a test gorilla.",
                                    "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                                    inst.driver)
        inst.gorilla.Register()
        
    def setUp(inst):
        inst.gorilla.Login()
        time.sleep(1)
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkPosts'))).click()
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkAddPost'))).click()
    
    def test_01_text_field_validation(self):
        # The "Text" field is required
        self.gorilla.AddPost('')
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div/div/div[1]/span'), '* Text is required'))

    def test_02_success_message_displays_after_post(self):
        # Success message should display after adding post
        my_post = '1st gorilla post'
        self.gorilla.AddPost(my_post)
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div/div/div[2]/span'), 'New post created successfully'))
        self.driver.get("http://localhost/socialnetwork/viewmyposts.php/")
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div/div[1]/p'), my_post))
        self.driver.get("http://localhost/socialnetwork/feed.php/")
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#feedPost p'), my_post))

    def tearDown(inst):
        inst.gorilla.Logout()
        
    @classmethod
    def tearDownClass(inst):
        # remove all test users
        inst.gorilla.Delete()
        # close browser
        inst.driver.quit()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)

    

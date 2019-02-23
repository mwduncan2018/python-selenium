import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestViewMyPostsPage(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(4)
        inst.driver.maximize_window()
        # create test user
        inst.gorilla = MikeBookUser("TestGorilla",
                               "GorillaLovin",
                               "testTwentySix",
                               "testTwentySix",
                               "I'm a test gorilla.",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               inst.driver)
        inst.gorilla.Register()
        
    def setUp(inst):
        inst.gorilla.Login()
        time.sleep(1)
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkPosts'))).click()
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkViewMyPosts'))).click()
    
    def test_01_if_no_posts_display_message_no_posts_to_view(self):
        # If the user has no posts, display "There are no posts to view"
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div/h4'), 'There are no posts to view'))

    def test_02_posts_should_be_ordered_newer_to_older(self):
        # Posts should be ordered newer at the top and older towards the bottom
        # upload posts as test data
        post_list = [
            '1st gorilla post',
            '2nd gorilla post',
            '3rd gorilla post',
            '4th gorilla post',
            '5th gorilla post',
            '6th gorilla post',
            '7th gorilla post',
            '8th gorilla post',
            '9th gorilla post',
            '10th gorilla post']
        for post in post_list:
            self.gorilla.AddPost(post)
        # navigate to the View My Posts page
        self.driver.get('http://localhost/socialnetwork/viewmyposts.php/')
        view_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.form-group p')
        # verify the number of posts displayed on the View My Posts page is correct
        self.assertEqual(len(post_list), len(view_list))
        # verify the order is newest (top) to oldest (bottom)
        for idx, element in enumerate(view_list):
            self.assertEqual(element.text, post_list[(len(post_list)-1)-idx])
        self.gorilla.RemoveAllPosts()

    def test_03_verify_one_post_displays_correctly(self):
        # verify one post displays correctly        
        # upload the poast as test data
        post_list = ['Single gorilla post']
        for post in post_list:
            self.gorilla.AddPost(post)
        # navigate to the View My Posts page
        self.driver.get('http://localhost/socialnetwork/viewmyposts.php/')
        view_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.form-group p')
        # verify the number of posts displayed on the View My Posts page is correct
        self.assertEqual(len(post_list), len(view_list))
        # verify the order is newest (top) to oldest (bottom)
        for idx, element in enumerate(view_list):
            self.assertEqual(element.text, post_list[(len(post_list)-1)-idx])
        self.gorilla.RemoveAllPosts()

    def tearDown(inst):
        inst.gorilla.Logout()
        
    @classmethod
    def tearDownClass(inst):
        # remove the test user
        inst.gorilla.Delete()
        # close browser
        inst.driver.quit()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)

    

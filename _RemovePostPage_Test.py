import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestRemovePostPage(unittest.TestCase):
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
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkRemovePost'))).click()

    def test_01_if_no_posts_then_display_a_message_saying_there_are_no_posts(self):
        # If there are no posts, "There are no posts to remove" should display
        # 1) Verify the message initially before any posts have been added
        # 2) Verify the message after posts have been added and then all posts have been deleted

        # 1 -- Verify message displays initially before any posts have been added
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'form h4'), 'There are no posts to remove'))
        # Add posts and then delete them all
        post_list = [
            '1st gorilla post',
            '2nd gorilla post']
        for post in post_list:
            self.gorilla.AddPost(post)
        self.gorilla.RemoveAllPosts()        
        # 2 -- Verify message displays after all posts have been deleted
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'form h4'), 'There are no posts to remove'))

    def test_02_verify_the_delete_button_removes_the_post_from_the_Remove_Post_Page_and_the_View_My_Posts_page(self):
        # Verify that a deleted post no longer displays on the Remove Post Page and the View My Post page
        # create test data
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
        # navigate to the Remove Post page
        self.driver.get('http://localhost/socialnetwork/removepost.php/')
        remove_btn_list = self.driver.find_elements(By.CSS_SELECTOR, '.btn-danger')
        # delete '3rd gorilla post', which should be the 8th element on the page
        del post_list[2]
        remove_btn_list[7].click()
        time.sleep(.25)
        # 1 -- verify the deleted post is no longer displayed on the Remove Post page
        remove_txt_list = self.driver.find_elements(By.CSS_SELECTOR, 'form p')
        for idx, element in enumerate(remove_txt_list):
            self.assertEqual(element.text, post_list[(len(post_list)-1)-idx])
        # navigate to View My Posts page
        self.driver.get('http:/localhost/socialnetwork/viewmyposts.php/')
        view_txt_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.form-group p')
        # verify the number of posts displayed on the View My Posts page is correct
        self.assertEqual(len(post_list), len(view_txt_list))
        # 2 -- verify the deleted post is no longer displayed on the View My Posts page
        for idx, element in enumerate(view_txt_list):
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

    

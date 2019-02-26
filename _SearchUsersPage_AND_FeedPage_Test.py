import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestSearchUsersPageAndFeedPage(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(4)
        inst.driver.maximize_window()
        # create test users
        inst.gorilla = MikeBookUser("TestGorilla",
                               "Gorilla",
                               "testTwentySix",
                               "testTwentySix",
                               "I'm a test gorilla.",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               inst.driver)
        inst.bach = MikeBookUser("TestBach",
                            "Bach",
                            "testTwentySeven",
                            "testTwentySeven",
                            "I'm a test musician.",
                            "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestBach01.jpeg",
                            inst.driver)
        inst.rhino = MikeBookUser("TestRhino",
                             "Rhino",
                             "testTwentyEight",
                             "testTwentyEight",
                             "I'm a test rhino.",
                             "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestRhino01.png",
                             inst.driver)
        inst.coke = MikeBookUser("TestCoke",
                             "Coke",
                             "testTwentyTwo",
                             "testTwentyTwo",
                             "Can't beat the real thing.",
                             "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_CocaCola_JPG.jpg",
                             inst.driver)
        inst.pepsi = MikeBookUser("TestPepsi",
                             "Pepsi",
                             "testTwo",
                             "testTwo",
                             "One at a time.",
                             "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_Pepsi_PNG.png",
                             inst.driver)
        inst.gorilla.Register()
        inst.bach.Register()
        inst.rhino.Register()
        inst.coke.Register()
        inst.pepsi.Register()

    def setUp(inst):
        inst.gorilla.Login()
        time.sleep(1)
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkSearchUsers'))).click()
    
    def test_01_all_users_other_than_the_currently_logged_in_user_should_be_displayed(self):
        # All users other than the currently logged in user should be displayed
        # 1 -- currently logged in user should not be displayed
        if (len(self.driver.find_elements(By.ID, self.gorilla.username)) != 0):
            print("\nError -- 'test_01...'\nVerify currently logged in user is not displayed on page... FAIL\n\n")
        # 2 -- all other users should be displayed on the page
        self.driver.find_element(By.ID, self.bach.username)
        self.driver.find_element(By.ID, self.rhino.username)
        self.driver.find_element(By.ID, self.coke.username)
        self.driver.find_element(By.ID, self.pepsi.username)
    
    def test_02_users_should_be_displayed_in_alphabetical_order(self):
        # From top to bottom, the users should be displayed in alphabetical order according to their name
        test_list = [
            self.bach.name,
            self.rhino.name,
            self.coke.name,
            self.pepsi.name]
        test_list.sort()
        page_list = []
        for user in (self.driver.find_elements_by_id('name')):
            page_list.append(user.text)
        self.assertEqual(page_list, test_list)

    def test_03_message_displays_if_currently_logged_in_user_is_the_only_user_that_exists(self):
        # If the currently logged in user is the only user that exists:
        # 1) No users should be displayed on the Search Users Page
        # 2) Message should be displayed stating "You are the only existing user. There are no other users to follow."
        self.bach.Delete()
        time.sleep(1)
        self.rhino.Delete()
        time.sleep(1)
        self.coke.Delete()
        time.sleep(1)
        self.pepsi.Delete()
        time.sleep(1)
        self.gorilla.Login()
        self.driver.get("http://localhost/socialnetwork/searchusers.php/")
        # 1 -- No users should be displayed
        if (len(self.driver.find_elements(By.ID, self.gorilla.username)) != 0):
            print("\nError -- 'test_03...'\nVerify no users are displayed when no users exist other than the currently logged in user...\n\n")
        # 2 -- Message displays
        WebDriverWait(self.driver, 2).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'h4'), 'You are the only existing user. There is no other user to follow.'))
        # Re-add the users that were deleted for this test
        self.bach.Register()
        self.rhino.Register()
        self.coke.Register()
        self.pepsi.Register()
    
    def test_04_verify_follow_and_unfollow_buttons_correct_behavior_on_Search_Users_Page_and_Feed_Page(self):
        # After clicking 'Follow' button
        # 1) 'Follow' button should change to 'Unfollow'
        # 2) Followed user should appear on current logged in user's Feed

        # test data
        list_03 = [
            '1st pepsi post',
            '2nd pepsi post',
            '3rd pepsi post']
        list_02 = [
            '1st rhino post',
            '2nd rhino post']
        list_01 = [
            '1st bach post',
            '2nd bach post']

        # upload test data
        self.gorilla.Logout()
        self.pepsi.Login()
        for post in list_03:
            self.pepsi.AddPost(post)
        self.pepsi.Logout()
        self.rhino.Login()
        for post in list_02:
            self.rhino.AddPost(post)
        self.rhino.Logout()
        self.bach.Login()
        for post in list_01:
            self.bach.AddPost(post)
        self.bach.Logout()

        # reverse lists
        list_03.reverse()
        list_02.reverse()
        list_01.reverse()

        # login as Pepsi and follow Pepsi
        self.gorilla.Login()
        self.gorilla.Follow(self.pepsi)
        # Verify Pepsi's button is now 'Unfollow'
        selector = '#' + self.pepsi.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Unfollow')
        # Verify the Posts of Pepsi are now on the Feed
        self.driver.get("http://localhost/socialnetwork/feed.php/")
        post_list = []
        for post in (self.driver.find_elements_by_css_selector('#feedPost p')):
            post_list.append(post.text)
        self.assertEqual(list_03, post_list)

        # Follow Rhino and Bach
        self.gorilla.Follow(self.rhino)
        self.gorilla.Follow(self.bach)
        # Verify their buttons are both "Unfollow"
        selector = '#' + self.rhino.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Unfollow')
        selector = '#' + self.bach.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Unfollow')
        # Verify that all posts display on the Feed and in the correct order
        self.driver.get("http://localhost/socialnetwork/feed.php/")
        test_list = []
        test_list = list_01 + list_02 + list_03
        post_list = []
        for post in (self.driver.find_elements_by_css_selector('#feedPost p')):
            post_list.append(post.text)
        self.assertEqual(test_list, post_list)

        # Unfollow Rhino
        self.gorilla.Follow(self.rhino)
        # Verify Rhino's button is "Follow"
        selector = '#' + self.rhino.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Follow')
        # Verify that posts display correctly
        self.driver.get("http://localhost/socialnetwork/feed.php/")
        test_list = []
        test_list = list_01 + list_03
        post_list = []
        for post in (self.driver.find_elements_by_css_selector('#feedPost p')):
            post_list.append(post.text)
        self.assertEqual(test_list, post_list)

        # Unfollow Pepsi
        self.gorilla.Follow(self.pepsi)
        # Verify their buttons are "Follow"
        selector = '#' + self.pepsi.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Follow')
        # Verify that posts display correctly
        self.driver.get("http://localhost/socialnetwork/feed.php/")
        test_list = []
        test_list = list_01
        post_list = []
        for post in (self.driver.find_elements_by_css_selector('#feedPost p')):
            post_list.append(post.text)
        self.assertEqual(test_list, post_list)

        # Unfollow Bach
        self.gorilla.Follow(self.bach)
        # Verify all buttons are "Follow"
        selector = '#' + self.pepsi.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Follow')
        selector = '#' + self.rhino.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Follow')
        selector = '#' + self.bach.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Follow')
        # Verify a message displays on the Feed Page -- "There are no posts to view"
        self.driver.get("http://localhost/socialnetwork/feed.php/")
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'h4'), 'There are no posts to view'))

        # Follow Coke
        self.gorilla.Follow(self.coke)
        # Verify Coke's button is "Unfollow"
        selector = '#' + self.coke.username + ' button.btn'
        button = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        self.assertEqual(button.text, 'Unfollow')
        # Verify a message displays on the Feed Page -- "There are no posts to view"
        self.driver.get("http://localhost/socialnetwork/feed.php/")
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'h4'), 'There are no posts to view'))

        # Remove all Posts created in this test
        self.gorilla.Logout()
        self.pepsi.Login()
        self.pepsi.RemoveAllPosts()
        self.pepsi.Logout()
        self.bach.Login()
        self.bach.RemoveAllPosts()
        self.bach.Logout()
        self.rhino.Login()
        self.rhino.RemoveAllPosts()
        self.rhino.Logout()
        self.gorilla.Login()
        
    def tearDown(inst):
        time.sleep(1)
        inst.gorilla.Logout()

    @classmethod
    def tearDownClass(inst):
        # remove the test user
        inst.gorilla.Delete()
        inst.bach.Delete()
        inst.rhino.Delete()
        inst.coke.Delete()
        inst.pepsi.Delete()
        # close browser
        inst.driver.quit()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)

    

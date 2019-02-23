import unittest, os, errno, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class TestNotLoggedIn(unittest.TestCase):
    def setUp(inst):
        # create a new Firefox session
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(10)
        inst.driver.maximize_window()
        # navigate to the PHP Social Network "Mike-Book"
        inst.driver.get("http://localhost/socialnetwork/default.php/")

    def test_MikeBook_link_should_redirect_to_home_page(self):
        # when not logged in, clicking the 'Mike-Book' link
        # should redirect to the Home Page
        self.driver.find_element_by_name('linkMikeBook').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/default.php/")

    def test_Register_link_should_redirect_to_register_page(self):
        # when not logged in, clicking the 'Register' link
        # should redirect to the Register Page
        self.driver.find_element_by_name('linkRegister').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/register.php/")

    def test_Login_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'Login' link
        # should redirect to the Login Page
        self.driver.find_element_by_name('linkLogin').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_Feed_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'Feed' link
        # should redirect to the Login Page
        self.driver.find_element_by_name('linkFeed').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_SearchUsers_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'Search Users' link
        # should redirect to the Login Page
        self.driver.find_element_by_name('linkSearchUsers').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_RemovePost_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'Remove Post' link
        # should redirect to the Login Page
        self.driver.find_element_by_xpath("//*[@id='myNavbar']/ul[1]/li[2]/a").click()
        self.driver.find_element_by_name('linkRemovePost').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_ViewMyPosts_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'View My Posts' link
        # should redirect to the Login Page
        self.driver.find_element_by_xpath("//*[@id='myNavbar']/ul[1]/li[2]/a").click()
        self.driver.find_element_by_name('linkViewMyPosts').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_AddPost_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'Add Post' link
        # should redirect to the Login Page
        self.driver.find_element_by_xpath("//*[@id='myNavbar']/ul[1]/li[2]/a").click()
        self.driver.find_element_by_name('linkAddPost').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_EditMyProfile_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'Edit My Profile' link
        # should redirect to the Login Page
        self.driver.find_element_by_xpath("//*[@id='myNavbar']/ul[1]/li[1]/a").click()
        self.driver.find_element_by_name('linkEditMyProfile').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_ViewMyProfile_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'View My Profile' link
        # should redirect to the Login Page
        self.driver.find_element_by_xpath("//*[@id='myNavbar']/ul[1]/li[1]/a").click()
        self.driver.find_element_by_name('linkViewMyProfile').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def test_DeleteMyProfile_link_should_redirect_to_login_page(self):
        # when not logged in, clicking the 'View My Profile' link
        # should redirect to the Login Page
        self.driver.find_element_by_xpath("//*[@id='myNavbar']/ul[1]/li[1]/a").click()
        self.driver.find_element_by_name('linkDeleteMyProfile').click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost/socialnetwork/login.php/")

    def tearDown(inst):
        inst.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)

    

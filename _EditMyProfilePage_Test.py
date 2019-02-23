import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestEditMyProfilePage(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(10)
        inst.driver.maximize_window()
        # create test users
        inst.gorilla = MikeBookUser("TestGorilla",
                                    "GorillaLovin",
                                    "testTwentySix",
                                    "testTwentySix",
                                    "I'm a test gorilla.",
                                    "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                                    inst.driver)
        inst.rhino = MikeBookUser("TestRhino",
                             "RhinoLovin",
                             "testTwentySeven",
                             "testTwentySeven",
                             "I live in Africa.",
                             "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestRhino01.png",
                             inst.driver)
        inst.gorilla.Register()
        inst.rhino.Register()
        
    def setUp(inst):
        inst.gorilla.Login()
        time.sleep(1)
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkProfile'))).click()
        WebDriverWait(inst.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkEditMyProfile'))).click()
    
    def test_01_verify_page_loads_with_fields_populated_correctly(self):
        # when the page loads, fields should be populated with the data of the current user that is logged in
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).get_attribute('value'), self.gorilla.name)
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).get_attribute('value'), self.gorilla.aboutMe)

    def test_02_image_field_validations(self):
        # Image Field Validations:
        # 1) validation message if file type is not JPG/JPEG/PNG
        self.fill_out_fields(self.gorilla.name, self.gorilla.aboutMe, "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\testDoc.txt")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[1]/div[2]/div[2]/span'), '* Only JPG, JPEG, and PNG files are allowed'))
        # 2) validation message if file already exists in database
        self.fill_out_fields(self.gorilla.name, self.gorilla.aboutMe, self.rhino.imageLocation)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[1]/div[2]/div[2]/span'), "* File already exists"))

    def test_03_image_field_accepts_JPEG_PNG_JPG_and_saves_successfully(self):
        # The image field should update successfully when given JPG/JPEG/PNG and that image file doesn't already exist in the database
        filepath = "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\"
        # 1) PNG successful update
        self.fill_out_fields(self.gorilla.name, self.gorilla.aboutMe, (filepath + "_Pepsi_PNG.png"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[2]/div/div/span'), 'Profile Updated'))
        # 2) JPG successful update
        self.fill_out_fields(self.gorilla.name, self.gorilla.aboutMe, (filepath + "_CocaCola_JPG.jpg"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[2]/div/div/span'), 'Profile Updated'))
        # 3) JPEG successful update
        self.fill_out_fields(self.gorilla.name, self.gorilla.aboutMe, (filepath + "_Sprite_JPEG.jpeg"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[2]/div/div/span'), 'Profile Updated'))

    def test_04_name_field_validations(self):
        # Name Field Validations:
        filepath = "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\"
        # 1) Required
        self.fill_out_fields("", self.gorilla.aboutMe, (filepath + "_Pepsi_PNG.png"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[1]/div[1]/div[1]/span'), '* Name is required'))
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).get_attribute('value'), '')
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).get_attribute('value'), self.gorilla.aboutMe)
        # 2) Less Than 51 Characters
        fiftyOneChars = "asdfzxcvjkasdfzxcvjkasdfzxcvjkasdfzxcvjkasdfzxcvjka"
        self.fill_out_fields(fiftyOneChars, self.gorilla.aboutMe, (filepath + "_Pepsi_PNG.png"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[1]/div[1]/div[1]/span'), ''))
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).get_attribute('value'), fiftyOneChars)
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).get_attribute('value'), self.gorilla.aboutMe)
        # 3) Only Letters Allowed
        someLetters = "test1234567890"
        self.fill_out_fields(someLetters, self.gorilla.aboutMe, (filepath + "_Pepsi_PNG.png"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[1]/div[1]/div[1]/span'), '* Name must contain only letters'))
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).get_attribute('value'), someLetters)
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).get_attribute('value'), self.gorilla.aboutMe)
        someSpecialChars = "test!@#$%^&*()_+"
        self.fill_out_fields(someSpecialChars, self.gorilla.aboutMe, (filepath + "_Pepsi_PNG.png"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[1]/div[1]/div[1]/span'), '* Name must contain only letters'))
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).get_attribute('value'), someSpecialChars)
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).get_attribute('value'), self.gorilla.aboutMe)
    
    def test_05a_name_field_updates_successfully_when_given_50_chars(self):
        # Name field updates successfully when given 50 chars
        filepath = "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\"
        modify_name = "sdfzxcvjkasdfzxcvjkasdfzxcvjkasdfzxcvjkasdfzxcvjka"
        self.fill_out_fields(modify_name, self.gorilla.aboutMe, (filepath + "_Pepsi_PNG.png"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[2]/div/div/span'), 'Profile Updated'))
        self.driver.get("http://localhost/socialnetwork/viewmyprofile.php/")
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div[2]/div[1]/p'), modify_name))
    
    def test_05b_name_field_updates_successfully_when_given_1_char(self):
        # Name field updates successfully when given 1 char
        filepath = "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\"
        modify_name = "G"
        self.fill_out_fields(modify_name, self.gorilla.aboutMe, (filepath + "_TestGorilla01.jpg"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[2]/div/div/span'), 'Profile Updated'))
        self.driver.get("http://localhost/socialnetwork/viewmyprofile.php/")
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div[2]/div[1]/p'), modify_name))

    def test_06_aboutMe_field_validations(self):
        filepath = "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\"
        # About Me is required
        self.fill_out_fields(self.gorilla.name, "", (filepath + "_Pepsi_PNG.png"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[1]/div[1]/div[2]/span'), '* About Me is required'))
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).get_attribute('value'), self.gorilla.name)
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).get_attribute('value'), '')

    def test_07_aboutMe_field_udpates_successfully(self):
        filepath = "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\"
        # About Me updates successfully when given correct input
        modify_aboutMe = "I'm a gorilla in the zoo zoo."
        self.fill_out_fields(self.gorilla.name, modify_aboutMe, (filepath + "_Sprite_JPEG.jpeg"))
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/form/div[2]/div/div/span'), 'Profile Updated'))
        self.driver.get("http://localhost/socialnetwork/viewmyprofile.php/")
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div[2]/div[3]/p'), modify_aboutMe))        
    
    def tearDown(inst):
        inst.gorilla.Logout()
        
    @classmethod
    def tearDownClass(inst):
        # remove all test users
        inst.gorilla.Delete()
        inst.rhino.Delete()
        # close browser
        inst.driver.quit()

    def fill_out_fields(self, name, aboutMe, imageLocation):
        # this method uploads an image for this test class, which is the EditMyProfile page
        # you must already be on the EditMyProfile page for this function to work
        time.sleep(1)
        element = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName')))
        element.clear()
        element.send_keys(name)
        element = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe')))
        element.clear()
        element.send_keys(aboutMe)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, 'html/body/div/form/div[1]/div[2]/div[2]/label'))).click()
        autoit = Dispatch("AutoItX3.Control")
        autoit.WinWaitActive("#32770", "File Upload", 1)
        autoit.ControlSetText("File Upload", " ", "Edit1", imageLocation)
        autoit.ControlClick("File Upload", " ", "Button1")
        
        

if __name__ == '__main__':
    unittest.main(verbosity=2)

    

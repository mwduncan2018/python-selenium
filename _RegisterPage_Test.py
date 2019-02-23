import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from _Classes import MikeBookUser

class TestRegisterPage(unittest.TestCase):
    def setUp(inst):
        # create a new Firefox session
        inst.driver = webdriver.Firefox()
        inst.driver.implicitly_wait(10)
        inst.driver.maximize_window()
        # navigate to the PHP Social Network "Mike-Book"
        inst.driver.get("http://localhost/socialnetwork/register.php/")

    def test_validation_for_fields_that_are_required(self):
        # Validation - the fields below are required
        self.driver.find_element_by_name('submit').click()
        # Name
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[1]/span"), "* Name is required"))
        # Username
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[2]/span"), "* Username is required"))
        # Password
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[3]/span"), "* Password is required"))
        # Confirm Password
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[4]/span"), "* Confirm Password is required"))
        # About Me
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[5]/span"), "* About Me is required"))
        # Image
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[6]/span"), "* Image is required"))

    def test_validation_for_fields_that_must_be_less_than_51_characters(self):
        # Validation - the fields below must be less than 51 characters
        fiftyOne = 'abcdefghijabcdefghijabcdefghijabcdefghijabcdefghija'
        self.driver.find_element_by_name('txtName').send_keys(fiftyOne)
        self.driver.find_element_by_name('txtUsername').send_keys(fiftyOne)
        self.driver.find_element_by_name('txtPassword').send_keys(fiftyOne)
        self.driver.find_element_by_name('submit').click()
        # Name
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[1]/span"), "* Name must be less than 51 characters"))
        # Username
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[2]/span"), "* Username must be less than 51 characters"))
        # Password
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[3]/span"), "* Password must be less than 51 characters"))

    def test_validation_for_fields_where_only_letters_are_allowed(self):
        # Validation - the fields below do not accept special chars
        invalidChars = '!@#$%^&*()_+{}|:"<>?[]\;,."specialChars'
        self.driver.find_element_by_name('txtName').send_keys(invalidChars)
        self.driver.find_element_by_name('txtUsername').send_keys(invalidChars)
        self.driver.find_element_by_name('txtPassword').send_keys(invalidChars)
        self.driver.find_element_by_name('submit').click()
        # Name
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[1]/span"), "* Name must contain only letters"))
        # Username
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[2]/span"), "* Username must contain only letters"))
        # Password
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[3]/span"), "* Password must contain only letters"))
        self.driver.find_element_by_name('txtName').clear()
        self.driver.find_element_by_name('txtUsername').clear()
        self.driver.find_element_by_name('txtPassword').clear()
        # ===================================================
        # Validation - the fields below do not accept numbers
        invalidNums = '1234567890numbers'
        self.driver.find_element_by_name('txtName').send_keys(invalidNums)
        self.driver.find_element_by_name('txtUsername').send_keys(invalidNums)
        self.driver.find_element_by_name('txtPassword').send_keys(invalidNums)
        self.driver.find_element_by_name('submit').click()
        # Name
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[1]/span"), "* Name must contain only letters"))
        # Username
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[2]/span"), "* Username must contain only letters"))
        # Password
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[3]/span"), "* Password must contain only letters"))
    
    def test_validation_username_cannot_already_exist_in_database(self):
        # Validation - Username cannot already exist in the database
        # step 1 = create a user "TestGorilla"
        gorilla = MikeBookUser("TestGorilla",
                               "TestGorilla",
                               "test",
                               "test",
                               "I'm a test gorilla",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               self.driver)
        gorilla.Register()
        # step 2 = navigate back to the Register Page and try to create another user with Username "TestGorilla"
        bach = MikeBookUser("TestBach",
                            "TestGorilla",
                            "test",
                            "test",
                            "I'm a musician",
                            "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                            self.driver)
        bach.Register()
        # step 3 = verify the validation message
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[2]/span"), "* Username cannot already exist"))
        # step 4 = remove the user created for this test
        gorilla.Delete()
    
    def test_validation_confirmPassword_field_must_match_password_field(self):
        # Validation = Confirm Password and Password fields do not match
        password = "myPassword"
        confirmPassword = "yourPassword"
        self.driver.find_element_by_name('txtPassword').send_keys(password)
        self.driver.find_element_by_name('txtConfirmPassword').send_keys(confirmPassword)
        self.driver.find_element_by_name('submit').click()
        wait = WebDriverWait(self.driver, 4)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[4]/span"), "* Confirm Password and Password must match"))

    def test_that_fields_keep_their_values_on_the_HTTP_POST_if_validations_have_fired(self):
        # After form submission and if validations fire, the fields should keep their values from before the form submission EXCEPT for Image Upload, which can forget it's value
        name = 'Jack'
        username = 'Septic-eye'
        password = 'xyz'
        confirmPassword = 'abc'
        aboutMe = 'Germany'
        self.driver.find_element_by_name('txtName').send_keys(name)
        self.driver.find_element_by_name('txtUsername').send_keys(username)
        self.driver.find_element_by_name('txtPassword').send_keys(password)
        self.driver.find_element_by_name('txtConfirmPassword').send_keys(confirmPassword)
        self.driver.find_element_by_name('areaAboutMe').send_keys(aboutMe)
        self.driver.find_element_by_name('submit').click()
        time.sleep(1)
        # Name
        self.assertEqual(self.driver.find_element_by_name('txtName').get_attribute('value'), name)
        # Username
        self.assertEqual(self.driver.find_element_by_name('txtUsername').get_attribute('value'), username)
        # Password
        self.assertEqual(self.driver.find_element_by_name('txtPassword').get_attribute('value'), password)
        # Confirm Password
        self.assertEqual(self.driver.find_element_by_name('txtConfirmPassword').get_attribute('value'), confirmPassword)
        # About Me
        self.assertEqual(self.driver.find_element_by_name('areaAboutMe').get_attribute('value'), aboutMe)

    def test_validation_invalid_file_type(self):
        # verify that attempting to upload an image with an invalid file type results in a validation message
        # step 1 - try to register a user with an invalid file type
        gorilla = MikeBookUser("TestGorilla",
                               "TestGorilla",
                               "test",
                               "test",
                               "I'm a test gorilla",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\testDoc.txt",
                               self.driver)
        gorilla.Register()
        # step 2 - verify the validation message
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[6]/span"), "* Only JPG, JPEG, and PNG files are allowed"))
        
    def test_validation_image_already_exists(self):
        # verify that attempting to upload an image that already exists results in a validation message
        # step 1 = create a new user with image "TestGorilla01.jpg"
        gorilla = MikeBookUser("TestGorilla",
                               "TestGorilla",
                               "test",
                               "test",
                               "I'm a test gorilla",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               self.driver)
        gorilla.Register()
        # step 2 = navigate back to the Register Page and try to create another user with "TestGorilla01.jpg"
        self.driver.get("http://localhost/socialnetwork/register.php/")
        bach = MikeBookUser("TestBach",
                               "TestBach",
                               "test",
                               "test",
                               "I'm a musician",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               self.driver)
        bach.Register()
        # step 3 = verify the validation message
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, "html/body/div/div[4]/div/form/div[6]/span"), "* File already exists"))
        # step 4 = remove the user created for this test
        gorilla.Delete()
    
    def test_that_PNG_JPG_JPEG_are_accepted_as_valid_types_for_the_image_field(self):
        # Verify that PNG, JPEG, and JPG are accepted as valid types for the image field
        # create the test users to verify those image types are accepted
        gorilla = MikeBookUser("TestGorillaJPG",
                               "TestGorillaJPG",
                               "test",
                               "test",
                               "I'm a test gorilla",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               self.driver)
        rhino = MikeBookUser("TestRhinoPNG",
                             "TestRhinoPNG",
                             "test",
                             "test",
                             "I'm a musician",
                             "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestRhino01.png",
                             self.driver)
        bach = MikeBookUser("TestBachJPEG",
                            "TestBachJPEG",
                            "test",
                            "test",
                            "I'm a musician",
                            "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestBach01.jpeg",
                            self.driver)
        gorilla.Register()
        bach.Register()
        rhino.Register()
        # delete the test users
        gorilla.Delete()
        bach.Delete()
        rhino.Delete()
    
    def test_register_page_loads_blank_register_page_after_successful_registration(self):
        # after a successful registration, the Register Page should load with all fields blank
        # step 1 - register a user
        gorilla = MikeBookUser("TestGorillaJPG",
                               "TestGorillaJPG",
                               "test",
                               "test",
                               "I'm a test gorilla",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               self.driver)
        gorilla.Register()
        # step 2 - verify we are on the Register Page and all fields are blank
        time.sleep(1)
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).get_attribute('value'), "")
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).get_attribute('value'), "")
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).get_attribute('value'), "")
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtConfirmPassword'))).get_attribute('value'), "")
        self.assertEqual(WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).get_attribute('value'), "")
        # step 3 - delete the test user
        gorilla.Delete()

    def test_register_page_should_display_success_message_after_registering_user(self):
        # after successful registration, the Register Page should load with a success message
        # step 1 - register a user
        gorilla = MikeBookUser("TestGorillaJPG",
                               "TestGorillaJPG",
                               "test",
                               "test",
                               "I'm a test gorilla",
                               "C:\\xampp\\htdocs\\_python_files\\test_php_socialnetwork\\Test_Images\\_TestGorilla01.jpg",
                               self.driver)
        gorilla.Register()
        # step 2 - verify the message is displayed
        WebDriverWait(self.driver, 4).until(EC.text_to_be_present_in_element((By.XPATH, 'html/body/div/div[4]/div/form/div[7]/span'), 'New record created successfully'))
        # step 3 - delete the test user
        gorilla.Delete()
    
    def tearDown(inst):
        inst.driver.quit()
        
    def silent_remove(self, filename):
        try:
            os.unlink(filename)
        except OSError as e:
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise
            pass

if __name__ == '__main__':
    unittest.main(verbosity=2)

    

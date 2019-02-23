import unittest, os, errno, time, autoit
from win32com.client import Dispatch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class MikeBookUser:

    def __init__(self, name, username, password, confirmPassword, aboutMe, imageLocation, driver):
        self.name = name
        self.username = username
        self.password = password
        self.confirmPassword = confirmPassword
        self.aboutMe = aboutMe
        self.imageLocation = imageLocation
        self.driver = driver
        
    def Register(self):
        self.driver.get("http://localhost/socialnetwork/register.php/")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtName'))).send_keys(self.name)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).send_keys(self.username)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).send_keys(self.password)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtConfirmPassword'))).send_keys(self.confirmPassword)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'areaAboutMe'))).send_keys(self.aboutMe)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, 'html/body/div/div[4]/div/form/div[6]/label'))).click()
        autoit = Dispatch("AutoItX3.Control")
        autoit.WinWaitActive("#32770", "File Upload", 1)
        autoit.ControlSetText("File Upload", " ", "Edit1", self.imageLocation)
        autoit.ControlClick("File Upload", " ", "Button1")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()

    def Delete(self):
        self.driver.get("http://localhost/socialnetwork/login.php/")
        wait = WebDriverWait(self.driver, 4)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).send_keys(self.username)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).send_keys(self.password)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        time.sleep(1)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkProfile'))).click()
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkDeleteMyProfile'))).click()
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        
    def Login(self):
        self.driver.get("http://localhost/socialnetwork/login.php/")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtUsername'))).send_keys(self.username)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtPassword'))).send_keys(self.password)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()

    def Logout(self):
        self.driver.get("http://localhost/socialnetwork/default.php/")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'linkLogout'))).click()
        
    def AddPost(self, post):
        self.driver.get("http://localhost/socialnetwork/addpost.php/")
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'txtText'))).send_keys(post)
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.NAME, 'submit'))).click()
        time.sleep(1.25)

    def RemovePost(self, postText):
        # 'postText' -- The text of the post to be deleted
        # Returns True if the post deleted successfully
        # Returns False if the post was not deleted
        self.driver.get("http://localhost/socialnetwork/removepost.php/")
        p_list = self.driver.find_elements_by_css_selector('div.form-group p')
        print("\n\np_list has " + str(len(p_list)) + " elements\n\n")
        if (not p_list): # if list is an empty sequence
            return False
        else:
            for element in p_list:
                print(str(element.text) + '\n')
            return True

    def RemoveAllPosts(self):
        self.driver.get("http://localhost/socialnetwork/removepost.php/")
        while (True):
            time.sleep(.5)
            try:
                WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-danger'))).click()
            except:
                return

    def Follow(self, user):
        self.driver.get("http://localhost/socialnetwork/searchusers.php/")
        selector = '#' + user.username + ' button.btn'
        WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
        time.sleep(1)
            

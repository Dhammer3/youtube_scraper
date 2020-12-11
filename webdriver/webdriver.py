from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class WebDriver:
    def __init__(self):
        self.driver=  webdriver.Chrome()
    
    def get(self, url):
        self.driver.get(url)
    
    def get_element(self, elem):
        self.driver.find_element_by_xpath(elem)
    
    def wait_for_elem_load(self, elem):
        loaded = False
        while not loaded:
            try:
                self.driver.get_element(elem)
                loaded= True
                print("element is loaded")
            except:
                continue
    
    def click_on_element(self, elem):
        self.wait_for_elem_load(elem)
        self.driver.find_element_by_xpath(elem).click()
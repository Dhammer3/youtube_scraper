from selenium import webdriver

import time

class WebDriver:
    def __init__(self):
        self.driver =  webdriver.Firefox()
    
    def get(self, url):
        self.driver.get(url)
    
    def get_element(self, *args):
        for elem in args:
            self.wait_for_elem_load(elem)
            try:
                return self.driver.find_element_by_xpath(elem)
            except:
                return 'None'
    
    def wait_for_elem_load(self, elem):
        loaded = False
        counter= 0
        while not loaded:
            try:
                self.driver.find_element_by_xpath(elem)
                loaded= True
            except:
                time.sleep(0.1)
            counter+=1
            if(counter > 50):
               break
    
    def get_element_text(self, elem):
        elem = self.get_element(elem)
        try:
            return elem.text
        except:
            return "None"
    
    def click(self, *args):
        for elem in args:
            self.wait_for_elem_load(elem)
            time.sleep(0.1)
            try:
                self.driver.find_element_by_xpath(elem).click()
            except:
                return
    
    def close(self):
        self.driver.close()
        
    def scroll(self, max_num_scrolls=5):
        old_position = 0
        new_position = None
        num_scrolls=0
        while new_position != old_position:
            # Get old scroll position
            old_position = self.driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
            # Sleep and Scroll
            time.sleep(1.2)
            self.driver.execute_script((
                    "var scrollingElement = (document.scrollingElement ||"
                    " document.body);scrollingElement.scrollTop ="
                    " scrollingElement.scrollHeight;"))
            # Get new position
            new_position = self.driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
            num_scrolls+=1
            if num_scrolls==max_num_scrolls:
                break
    
    def find_elements_by_tag_name(self, tag_name):
        return self.driver.find_elements_by_tag_name(tag_name)

    def find_element_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

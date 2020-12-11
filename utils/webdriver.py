from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class WebDriver:
    def __init__(self):
        self.driver =  webdriver.Chrome()
        
    
    def get(self, url):
        self.driver.get(url)
    
    def get_element(self, elem):
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
                print("element is loaded")
            except:
                time.sleep(0.2)
                print("element not loaded")
                
            counter+=1
            
            if(counter > 50):
               break
    
    def get_element_text(self, elem):
        elem = self.get_element(elem)
        try:
            return elem.text
        except:
            return "None"

    def get_multiple_elements(self, elem):
        self.wait_for_elem_load(elem)
        return self.driver.find_elements_by_xpath(elem)
    
    def click(self, elem):
        self.wait_for_elem_load(elem)
        time.sleep(0.2)
        try:
            self.driver.find_element_by_xpath(elem).click()
        except:
            return
  
    
    def close(self):
        self.driver.close()
        
    def scroll_to_bottom(self):
        old_position = 0
        new_position = None
        MAX_NUM_SCROLLS=5
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



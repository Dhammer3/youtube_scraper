from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time



def scroll_to_bottom(driver):
    old_position = 0
    new_position = None
    MAX_NUM_SCROLLS=10
    num_scrolls=0
    while new_position != old_position:
        if(num_scrolls>=MAX_NUM_SCROLLS):
                break
        #Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"))
        num_scrolls+=1
        
def scroll_to_one_year(driver):
    old_position = 0
    new_position = None
    MAX_NUM_SCROLLS=5
    num_scrolls=0
    upload_time = driver.find_element_by_xpath("//div[@id='metadata-line']/span[@class='style-scope ytd-grid-video-renderer' and 2]").text
    print(upload_time[5])
    while upload_time != "12 months ago":
        upload_time = driver.find_element_by_xpath("//div[@id='metadata-line']/span[@class='style-scope ytd-grid-video-renderer' and 2]").text

        print(upload_time)
            
        # if(num_scrolls>=MAX_NUM_SCROLLS):
        #         break
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"))
        num_scrolls+=1
        
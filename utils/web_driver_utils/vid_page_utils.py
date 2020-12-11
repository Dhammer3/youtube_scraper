from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class CONSTANTS():
    NUMBER_LIKES="//ytd-toggle-button-renderer[1]/a[@class='yt-simple-endpoint style-scope ytd-toggle-button-renderer' and 1]/yt-formatted-string[@id='text' and @class='style-scope ytd-toggle-button-renderer style-text' and 1]"
    NUMBER_DISLIKES="//ytd-toggle-button-renderer[2]/a[@class='yt-simple-endpoint style-scope ytd-toggle-button-renderer' and 1]/yt-formatted-string[@id='text' and @class='style-scope ytd-toggle-button-renderer style-text' and 1]"
    VIEWS="//span[@class='view-count style-scope yt-view-count-renderer']"
    UPLOAD_DATE="//div[@id='date']/yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer' and 1]"
    TITLE="//h1/yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer' and 1]"
    DESC="//div[@id='description']"
    DURATION="//span[@class='ytp-time-duration']"
    NUM_COMMENTS="//yt-formatted-string[@class='count-text style-scope ytd-comments-header-renderer']"
    CHANNEL_NAME="//yt-formatted-string[@id='text']/a[@class='yt-simple-endpoint style-scope yt-formatted-string' and 1]"
    CHANNEL_SUBS="//yt-formatted-string[@id='owner-sub-count']"

def convert_text_to_num(subs):
        subs=subs.text
        sum=""
        i=0
        char=subs[0]
        while(char!="K"):
            if(char!='.' or char!="K"):
                sum+=subs[i]
            i+=1
            char= subs[i]

        if(char=="K"):
            return int(sum)*1000
        if(char=="M"):
            return int(sum)*1000000
        return int(sum)

def get_video_likes(on_page_driver):
    item= on_page_driver.find_element_by_xpath(CONSTANTS.NUMBER_LIKES)
    return convert_text_to_num(item)

def get_video_dislikes(on_page_driver):
    item= on_page_driver.find_element_by_xpath(CONSTANTS.NUMBER_DISLIKES)
    return convert_text_to_num(item)

def get_video_views(on_page_driver):
    item= on_page_driver.find_element_by_xpath(CONSTANTS.VIEWS)
    return item

def get_video_upload_date(on_page_driver):
    item= on_page_driver.find_element_by_xpath(CONSTANTS.UPLOAD_DATE)
    return item

def get_video_title(on_page_driver):
    item= on_page_driver.find_element_by_xpath(CONSTANTS.TITLE)
    return item

def get_video_description(on_page_driver):
    item= on_page_driver.find_element_by_xpath(CONSTANTS.DESC)
    return item
def get_video_duration(on_page_driver):
    return on_page_driver.find_element_by_xpath(CONSTANTS.DURATION)

def get_video_num_comments(on_page_driver):
    return on_page_driver.find_element_by_xpath(CONSTANTS.NUM_COMMENTS)

def get_video_channel_name(on_page_driver):
    return on_page_driver.find_element_by_xpath(CONSTANTS.CHANNEL_NAME)

def get_video_channel_subs(driver):
    item= driver.find_element_by_xpath(CONSTANTS.CHANNEL_SUBS)
    return item.text


driver  = webdriver.Chrome()
driver.get('https://www.youtube.com/watch?v=6joO2-n8wJk&t=562s')
time.sleep(5)
item= driver.find_element_by_xpath(CONSTANTS.CHANNEL_SUBS)
print(item.text)
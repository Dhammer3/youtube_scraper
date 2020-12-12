from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium_utils import scroll_to_bottom
import random
from x_path_constants import X_PATH_CONSTANTS
from text_conversion import convert_text_to_num
import pandas as pd
from webdriver import WebDriver
# from selenium import webdriver from selenium.webdriver.chrome.options import Options

# import time
# chrome_options = Options()
# #chrome_options.add_argument("--disable-extensions")
# #chrome_options.add_argument("--disable-gpu")
# #chrome_options.add_argument("--no-sandbox") # linux only
# chrome_options.add_argument("--headless")

class CSV_COLS():
    LIKES="LIKES"
    DISLIKES="DISLIKES"
    VIEWS="VIEWS"
    UPLOAD_DATE="UPLOAD_DATE"
    TITLE="TITLE"
    DESCRIPTION="DESCRIPTION"
    DURATION="DURATION"
    NUM_COMMENTS="NUM_COMMENTS"
    CHANNEL_SUBS="CHANNEL_SUBS"
    URL="URL"
    CHANNEL_NAME="CHANNEL_NAME"
    TRANSCRIPT="TRANSCRIPT"

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
    SHOW_MORE="//yt-formatted-string[@class='more-button style-scope ytd-video-secondary-info-renderer']"
    SKIP_ADD_BUTTON="/html/body/div[2]/div[2]/div[2]/div/div[3]/form/div/input"
   
class wait_for_page_load(object):
  def __init__(self, browser):
    self.browser = browser
  def __enter__(self):
    self.old_page = self.browser.find_element_by_tag_name('html')
  def page_has_loaded(self):
    new_page = self.browser.find_element_by_tag_name('html')
    return new_page.id != self.old_page.id
  def __exit__(self, *_):
    wait_for(self.page_has_loaded)

class youtube_crawler():
    LIKES="LIKES"
    DISLIKES="DISLIKES"
    VIEWS="VIEWS"
    UPLOAD_DATE="UPLOAD_DATE"
    TITLE="TITLE"
    DESCRIPTION="DESCRIPTION"
    DURATION="DURATION"
    NUM_COMMENTS="NUM_COMMENTS"
    CHANNEL_SUBS="CHANNEL_SUBS"
    URL="URL"
    CHANNEL_NAME="CHANNEL_NAME"
    TRANSCRIPT="TRANSCRIPT"

    def __init__(self):
        self.__word_list=[]
        self.__df__=pd.DataFrame(columns=[CSV_COLS.URL,CSV_COLS.TITLE, CSV_COLS.DESCRIPTION, CSV_COLS.LIKES, CSV_COLS.DISLIKES, CSV_COLS.VIEWS, CSV_COLS.UPLOAD_DATE, CSV_COLS.DURATION, 
                                          CSV_COLS.NUM_COMMENTS, CSV_COLS.CHANNEL_NAME, CSV_COLS.CHANNEL_SUBS, CSV_COLS.URL, CSV_COLS.TRANSCRIPT])
        
    #return a df with 2 cols: |timestamp|_|text| 
    def get_video_transcript(self, youtube_url):
        on_page_driver = WebDriver()
        on_page_driver.get(youtube_url)
        transcript=[]
        time.sleep(5)
        on_page_driver.click(CONSTANTS.SKIP_ADD_BUTTON)
        time.sleep(2)
        on_page_driver.click(CONSTANTS.SHOW_MORE)
        on_page_driver.click(X_PATH_CONSTANTS.OPEN_OPTIONS_BUTTON)
        on_page_driver.click(X_PATH_CONSTANTS.OPEN_TRANSCRIPT_BUTTON)
        transcript = on_page_driver.get_multiple_elements(X_PATH_CONSTANTS.TRANSCRIPT)
        
        likes = on_page_driver.get_element_text(CONSTANTS.NUMBER_LIKES)
        dislikes = on_page_driver.get_element_text(CONSTANTS.NUMBER_DISLIKES)
        views = on_page_driver.get_element_text(CONSTANTS.VIEWS)
        upload_date = on_page_driver.get_element_text(CONSTANTS.UPLOAD_DATE)
        title = on_page_driver.get_element_text(CONSTANTS.TITLE)
        description = on_page_driver.get_element_text(CONSTANTS.DESC)
        duration = on_page_driver.get_element_text(CONSTANTS.DURATION)
        num_comments =on_page_driver.get_element_text(CONSTANTS.NUM_COMMENTS)
        channel_name =on_page_driver.get_element_text(CONSTANTS.CHANNEL_NAME)
        channel_subs =on_page_driver.get_element_text(CONSTANTS.CHANNEL_SUBS)
        #timestamp = on_page_driver.get_element_text(X_PATH_CONSTANTS.TIMESTAMP)
        
            
        total_trans=[]
        for e in transcript:
            total_trans.append(e.text)
        out_dict={CSV_COLS.URL:youtube_url, CSV_COLS.TITLE: title,CSV_COLS.DESCRIPTION:description,  CSV_COLS.LIKES:likes, CSV_COLS.DISLIKES:dislikes, CSV_COLS.VIEWS:views,
                CSV_COLS.UPLOAD_DATE:upload_date, CSV_COLS.DURATION:duration, CSV_COLS.NUM_COMMENTS:num_comments, 
                CSV_COLS.CHANNEL_NAME:channel_name, CSV_COLS.CHANNEL_SUBS:channel_subs, CSV_COLS.URL:youtube_url, CSV_COLS.TRANSCRIPT:total_trans}
        on_page_driver.close()
        self.__df__=self.__df__.append(out_dict, ignore_index=True)
        self.__df__.to_html('temp.html')
        self.__df__.to_csv('output.csv')

    def get_list_of_videos_on_channel(self, youtube_url):
        driver = webdriver.Chrome()
        driver.get(youtube_url)
        scroll_to_bottom(driver)
        time.sleep(4)
        videos = driver.find_elements_by_tag_name('a')
        list_of_videos =[]
        for e in videos:
            a = e.get_attribute('href')
            if(a !=None and "redirect" not in a):
                if("watch" in a and a not in list_of_videos):
                    list_of_videos.append(a)
        driver.close()
       
        return list_of_videos
        
    def get_all_video_transcripts_from_channel(self, youtube_url):
        list_of_videos=self.get_list_of_videos_on_channel(youtube_url)
        
        joined_list=[]
        for video_url in list_of_videos:
            try:
                self.get_video_transcript(video_url)
            except KeyboardInterrupt:
                print("stopped due to keyboard interrupt")
                with open("words.txt", "a") as output:
                    output.write(str(joined_list))
                return

   
    def get_channel_sub_count(self, youtube_url):
        driver = webdriver.Chrome()
        driver.get(youtube_url)
        subs = driver.find_element_by_xpath("//yt-formatted-string[@id='subscriber-count']")
        subs = convert_text_to_num(subs)
        (subs)
        driver.close()
        return subs

    def get_video_view_count(self, youtube_url):
        driver = webdriver.Chrome()
        driver.get(youtube_url)
        time.sleep(2)
        views = driver.find_element_by_xpath("//span[@class='view-count style-scope yt-view-count-renderer']")
        processed= views.text
        processed = processed.replace('views', '')
        driver.close()
        return processed

yt= youtube_crawler()
t=yt.get_all_video_transcripts_from_channel("https://www.youtube.com/c/msnbc/videos")
#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
class WebDriver():
    def __init__(self, webdriver):
        self.driver =  webdriver.Firefox()
    
    def __del__(self):
        self.driver.close()

    def get(self, url):
        self.driver.get(url)
    
    def get_element(self, elem):
        self.wait_for_elem_load(elem)
        try:
            return self.driver.find_element_by_xpath(elem)
        except:
            return {'text':'None'}
    
    def get_multiple_elements(self, elem):
        self.wait_for_elem_load(elem)
        return self.driver.find_elements_by_xpath(elem)
    
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
            return 'None'
    
    def click(self, *args):
        for elem in args:
            self.wait_for_elem_load(elem)
            time.sleep(0.1)
            try:
                self.driver.find_element_by_xpath(elem).click()
            except:
                pass
    
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

class X_PATH_CONSTANTS():
    TIMESTAMP="//div[@class='cue-group style-scope ytd-transcript-body-renderer']/div[@class='cue-group-start-offset style-scope ytd-transcript-body-renderer' and 1]"
    TRANSCRIPT ="//div[@class='cue style-scope ytd-transcript-body-renderer']"
    OPEN_TRANSCRIPT_BUTTON="//yt-formatted-string[@class='style-scope ytd-menu-service-item-renderer']"
    OPEN_OPTIONS_BUTTON ="//ytd-menu-renderer[@class='style-scope ytd-video-primary-info-renderer']/yt-icon-button[@id='button' and @class='dropdown-trigger style-scope ytd-menu-renderer' and 1]/button[@id='button' and @class='style-scope yt-icon-button' and 1]/yt-icon[@class='style-scope ytd-menu-renderer' and 1]"
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
    SUBSCRIBERS ="//yt-formatted-string[@id='subscriber-count']"

class youtube_crawler(WebDriver):
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

    def __init__(self, webdriver):
        self.__word_list=[]
        self.__df__=pd.DataFrame(columns=[CSV_COLS.URL,CSV_COLS.TITLE, CSV_COLS.DESCRIPTION, CSV_COLS.LIKES, CSV_COLS.DISLIKES, CSV_COLS.VIEWS, CSV_COLS.UPLOAD_DATE, CSV_COLS.DURATION, 
                                          CSV_COLS.NUM_COMMENTS, CSV_COLS.CHANNEL_NAME, CSV_COLS.CHANNEL_SUBS, CSV_COLS.URL, CSV_COLS.TRANSCRIPT])
        
        self.driver=webdriver

    def __del__(self):
        self.driver.close()

    def get_video_links(self, driver):
        videos = self.driver.find_elements_by_tag_name('a')
        list_of_videos =[]
        for e in videos:
            a = e.get_attribute('href')
            if(a !=None and "redirect" not in a):
                if("watch" in a and a not in list_of_videos):
                    list_of_videos.append(a)
        return list_of_videos

    def upload_time_is_recent(self, upload_time):
        if upload_time == []:
            return False
        upload_time=upload_time[0]
        unacceptable_measures=['month','year','months','years']
        for measure in unacceptable_measures:
            if measure in upload_time:
                return False
        return True    

    def get_recent_video_links(self, driver):
        videos = self.driver.find_elements_by_id('video-title')
        list_of_videos ={'links':[],'upload_times':[]}
        for e in videos:
            link = e.get_attribute('href')
            label= e.get_attribute('aria-label')
            upload_time =re.findall(r"[\d]+[\s][\w]+\b ago\b",label)
            if self.upload_time_is_recent(upload_time) :
                list_of_videos['links'].append(link)
                list_of_videos['upload_times'].append(upload_time[0])
        return list_of_videos

    def process_transcript(self, transcript):
        total_trans=[]
        for e in transcript:
            total_trans.append(e.text)
        return total_trans

    def append_df(self, out_dict):
        self.__df__=self.__df__.append(out_dict, ignore_index=True)

    def make_csv(self):
        self.__df__.to_csv('output.csv')
    
    def make_html(self, out_dict):
        self.__df__.to_html('temp.html')
        
    def get_video_transcript(self, youtube_url):
        self.driver.get(youtube_url)
        self.driver.click(
        CONSTANTS.SKIP_ADD_BUTTON,
        CONSTANTS.SHOW_MORE,
        X_PATH_CONSTANTS.OPEN_OPTIONS_BUTTON,
        X_PATH_CONSTANTS.OPEN_TRANSCRIPT_BUTTON)
        
        transcript = self.driver.get_multiple_elements(X_PATH_CONSTANTS.TRANSCRIPT)
        transcript = self.process_transcript(transcript)
        
        likes = self.driver.get_element_text(CONSTANTS.NUMBER_LIKES)
        dislikes = self.driver.get_element_text(CONSTANTS.NUMBER_DISLIKES)
        views = self.driver.get_element_text(CONSTANTS.VIEWS)
        upload_date = self.driver.get_element_text(CONSTANTS.UPLOAD_DATE)
        title = self.driver.get_element_text(CONSTANTS.TITLE)
        description = self.driver.get_element_text(CONSTANTS.DESC)
        duration = self.driver.get_element_text(CONSTANTS.DURATION)
        num_comments =self.driver.get_element_text(CONSTANTS.NUM_COMMENTS)
        channel_name =self.driver.get_element_text(CONSTANTS.CHANNEL_NAME)
        channel_subs =self.driver.get_element_text(CONSTANTS.CHANNEL_SUBS)
        #timestamp = self.driver.get_element_text(X_PATH_CONSTANTS.TIMESTAMP)
        
        out_dict={CSV_COLS.URL:youtube_url, CSV_COLS.TITLE: title,CSV_COLS.DESCRIPTION:description,  CSV_COLS.LIKES:likes, CSV_COLS.DISLIKES:dislikes, CSV_COLS.VIEWS:views,
                CSV_COLS.UPLOAD_DATE:upload_date, CSV_COLS.DURATION:duration, CSV_COLS.NUM_COMMENTS:num_comments, 
                CSV_COLS.CHANNEL_NAME:channel_name, CSV_COLS.CHANNEL_SUBS:channel_subs, CSV_COLS.URL:youtube_url, CSV_COLS.TRANSCRIPT:total_trans}
        
        self.append_df(out_dict)
        self.make_csv()

    def get_list_of_videos_on_channel(self, youtube_url):
        self.driver.get(youtube_url)
        self.driver.scroll()
        videos = self.driver.find_elements_by_tag_name('a')
        list_of_videos =[]
        list_of_videos=self.get_video_links(driver)
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
        self.driver.get(youtube_url)
        subs = self.driver.find_element_by_xpath(CONSTANTS.SUBSCRIBERS)
        return subs

    def get_video_view_count(self, youtube_url):
        self.driver.get(youtube_url)
        views = self.driver.find_element_by_xpath(CONSTANTS.VIEWS)
        processed= views.text
        processed = processed.replace('views', '')
        return processed

    def get_recent_videos_from_query(self, query):
        url = f"https://www.youtube.com/results?search_query={query}&sp=CAI%253D"
        self.driver.get(url)
        self.driver.scroll()
        dict= self.get_recent_video_links(self.driver)
        return dict
        

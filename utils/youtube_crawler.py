#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re
class WebDriver():
    def __init__(self):
        self.driver =  webdriver.Firefox()
        self.current_url = ""
    
    def __del__(self):
        self.driver.close()

    def get(self, url):
        self.current_url = url
        self.driver.get(url)
    
    def get_element(self, elem, findByID=False):
        self.wait_for_elem_load(elem, findByID)
        try:
            if findByID:
                return self.driver.find_element_by_id(elem)
            else:
                return self.driver.find_element_by_xpath(elem)
        except:
            return {'text':'None'}
    
    
    def get_multiple_elements(self, elem, findByID=False):
        self.wait_for_elem_load(elem, findByID)
        if findByID:
            return self.driver.find_elements_by_id(elem)
        return self.driver.find_elements_by_xpath(elem)
    
    def wait_for_elem_load(self, elem, findByID=False):
        loaded = False
        counter= 0
        while not loaded:
            try:
                if findByID:
                    self.driver.find_element_by_id(elem)
                else:
                    self.driver.find_element_by_xpath(elem)
                loaded= True
            except:
                #the element is not on the page yet
                time.sleep(0.1)
                #the element may be lazy loaded in, so we scroll to trigger it.
                self.single_scroll()
            counter+=1
            #allow up to 5 seconds for the element to load
            if(counter > 25): 
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
    
    def get_screen_position(self):
        return self.driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
    
    def single_scroll(self):
        self.driver.execute_script((
        "var scrollingElement = (document.scrollingElement ||"
        " document.body);scrollingElement.scrollTop ="
        " scrollingElement.scrollHeight;"))
        
    def scroll(self, max_num_scrolls=5):
        old_position = 0
        new_position = None
        num_scrolls=0
        
        while new_position != old_position:
            old_position = self.get_screen_position()
            time.sleep(1.2)
            new_position = self.get_screen_position()
            num_scrolls+=1
            self.single_scroll()
            if num_scrolls==max_num_scrolls:
                break
    
    def find_elements_by_tag_name(self, tag_name):
        return self.driver.find_elements_by_tag_name(tag_name)

    def find_element_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

class X_PATH_CONSTANTS():
    class TRANSCRIPT:
        TIMESTAMP="//div[@class='cue-group style-scope ytd-transcript-body-renderer']/div[@class='cue-group-start-offset style-scope ytd-transcript-body-renderer' and 1]"
        TRANSCRIPT ="//div[@class='cue style-scope ytd-transcript-body-renderer']"
        OPEN_TRANSCRIPT_BUTTON="//yt-formatted-string[@class='style-scope ytd-menu-service-item-renderer']"
        OPEN_OPTIONS_BUTTON ="//ytd-menu-renderer[@class='style-scope ytd-video-primary-info-renderer']/yt-icon-button[@id='button' and @class='dropdown-trigger style-scope ytd-menu-renderer' and 1]/button[@id='button' and @class='style-scope yt-icon-button' and 1]/yt-icon[@class='style-scope ytd-menu-renderer' and 1]"
    class COMMENTS:
        NUMBER_COMMENTS="//yt-formatted-string[@class='count-text style-scope ytd-comments-header-renderer']"
        COMMENT_BLOCK="//div[@id='main' and @class='style-scope ytd-comment-renderer']"
        VIEW_REPLIES_BUTTON="//yt-formatted-string[@id='text' and @class='style-scope ytd-button-renderer']"
        
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
        self.__word_list = []
        self.__df__ = pd.DataFrame(columns=[CSV_COLS.URL,CSV_COLS.TITLE, CSV_COLS.DESCRIPTION, CSV_COLS.LIKES, CSV_COLS.DISLIKES, CSV_COLS.VIEWS, CSV_COLS.UPLOAD_DATE, CSV_COLS.DURATION, 
                                          CSV_COLS.NUM_COMMENTS, CSV_COLS.CHANNEL_NAME, CSV_COLS.CHANNEL_SUBS, CSV_COLS.URL, CSV_COLS.TRANSCRIPT])
        
        self.driver = webdriver
        self.url = None

    def __del__(self):
        self.url=None
        self.driver.close()

    def get_video_links(self):
        videos = self.driver.find_elements_by_tag_name('a')
        list_of_videos =[]
        for video in videos:
            link = video.get_attribute('href')
            if(link !=None and "redirect" not in link):
                if("watch" in link and link not in list_of_videos):
                    list_of_videos.append(link)
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

    def get_recent_video_links(self):
        videos = self.driver.get_multiple_elements('video-title',findByID=True )
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

    def make_csv(self,filename="output.csv"):
        self.__df__.to_csv(filename)
    
    def make_html(self, filename="output.html"):
        self.__df__.to_html(filename)
    
    def make_txt(self, filename="output.txt", words=[]):
        with open("words.txt", "a") as output:
            output.write(str(words))
    
    def get(self, youtube_url):
        self.url=youtube_url
        self.driver.get(youtube_url)
    
    def get_video_transcript(self):
        self.driver.click(
        CONSTANTS.SKIP_ADD_BUTTON,
        CONSTANTS.SHOW_MORE,
        X_PATH_CONSTANTS.TRANSCRIPT.OPEN_OPTIONS_BUTTON,
        X_PATH_CONSTANTS.TRANSCRIPT.OPEN_TRANSCRIPT_BUTTON)
        
        transcript = self.driver.get_multiple_elements(X_PATH_CONSTANTS.TRANSCRIPT.TRANSCRIPT)
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
        
        out_dict={CSV_COLS.URL:self.url, CSV_COLS.TITLE: title,CSV_COLS.DESCRIPTION:description,  CSV_COLS.LIKES:likes, CSV_COLS.DISLIKES:dislikes, CSV_COLS.VIEWS:views,
                CSV_COLS.UPLOAD_DATE:upload_date, CSV_COLS.DURATION:duration, CSV_COLS.NUM_COMMENTS:num_comments, 
                CSV_COLS.CHANNEL_NAME:channel_name, CSV_COLS.CHANNEL_SUBS:channel_subs, CSV_COLS.URL:self.url, CSV_COLS.TRANSCRIPT:transcript}
        
        self.append_df(out_dict)
        # self.make_csv()

    def get_list_of_videos_on_channel(self):
        self.driver.scroll()
        videos = self.driver.find_elements_by_tag_name('a')
        list_of_videos =[]
        list_of_videos=self.get_video_links()
        return list_of_videos
        
    def get_all_video_transcripts_from_channel(self, youtube_url):
        list_of_videos=self.get_list_of_videos_on_channel(youtube_url)
        joined_list=[]
        for video_url in list_of_videos:
            try:
                self.get(video_url)
                self.get_video_transcript()
            except KeyboardInterrupt:
                print("stopped due to keyboard interrupt")
                return

    def get_channel_sub_count(self):
        subs = self.driver.get_element_text(CONSTANTS.SUBSCRIBERS)
        return subs

    def get_video_view_count(self):
        views = self.driver.get_element_text(CONSTANTS.VIEWS)
        processed = views.replace('views', '')
        processed = processed.replace(',', '')
        processed = int(processed)
        
        return processed

    def get_recent_videos_from_query(self, query):
        url = f"https://www.youtube.com/results?search_query={query}&sp=CAI%253D"
        self.get(url)
        self.driver.scroll()
        dict= self.get_recent_video_links()
        return dict
    
    def convert_comment(self, comment):
        comment_block=comment.split('\n')
        
        username = comment_block[0]
        time_posted = comment_block[1]
        comment_text = comment_block[2]
        
        try:
            number_likes=comment_block[3]
        except:
            number_likes=0

        converted ={'username':username,
                    'time_posted':time_posted,
                    'comment_text':comment_text,
                    'number_likes':number_likes
                    }
        return converted
    
    def get_all_comments_from_video(self):
        
        total_comments = self.driver.get_element_text(X_PATH_CONSTANTS.COMMENTS.NUMBER_COMMENTS)
        
        #parse the string
        total_comments=total_comments.replace(' Comments','')
        if "," in total_comments:
            total_comments=int(total_comments.replace(',',''))
        total_comments = int(total_comments)
        
        number_comments_shown = len(self.driver.get_multiple_elements(X_PATH_CONSTANTS.COMMENTS.COMMENT_BLOCK))
        
        #we need to keep scrolling until all of the comments are lazy loaded in. 
        while total_comments != number_comments_shown:
            number_comments_shown = len(self.driver.get_multiple_elements(X_PATH_CONSTANTS.COMMENTS.COMMENT_BLOCK))        #now we can collect the information
            old_position = self.driver.get_screen_position()
            self.driver.single_scroll()
            time.sleep(1.2)
            new_position = self.driver.get_screen_position()
            #youtube will not lazy-load anymore comments
            if new_position == old_position:
                break
        comment_blocks=self.driver.get_multiple_elements(X_PATH_CONSTANTS.COMMENTS.COMMENT_BLOCK)
        #the comment block contains the username, comment, and number of likes/dislikes seperated by '\n'
        
        #this line takes a while
        parsed_comment_blocks=list(map(lambda x:x.text, comment_blocks))
        #convert the single dimension list to a list of comment dictionaries
        parsed_comment_blocks = list(map(lambda comment:self.convert_comment(comment), parsed_comment_blocks))
        return parsed_comment_blocks
    

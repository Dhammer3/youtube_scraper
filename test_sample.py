import unittest
from utils.youtube_crawler import youtube_crawler, WebDriver


@classmethod
def setUpClass(youtube_crawler):
    wb = WebDriver()
    yt = youtube_crawler(wb)


class TestYoutubeCrawler(unittest.TestCase):
    
    def setUp(self):
        self.wb = WebDriver()
        self.yt = youtube_crawler(self.wb)
        self.video_url = 'https://www.youtube.com/watch?v=xCixkaXrVMI'
        self.channel_url ='https://www.youtube.com/c/ImdadAhad/videos'
    
    def tearDown(self):
        del self.yt
    
    @unittest.skip("demonstrating skipping")   
    def test_get(self):
        url = self.video_url
        self.yt.get(url)
        assert self.yt.url == url
    
    @unittest.skip("demonstrating skipping")
    def test_get_video_transcript(self):
        url = self.video_url
        self.yt.get(url)
        self.yt.get_video_transcript()
        df = self.yt.__df__
        rows = df.iloc[:]
        assert len(rows) != 0

    @unittest.skip("demonstrating skipping")
    def test_get_list_of_videos_on_channel(self):
        url = self.channel_url
        self.yt.get(url)
        channel_videos = self.yt.get_list_of_videos_on_channel()
        assert(len(channel_videos)!= 0)
    
    @unittest.skip("demonstrating skipping")
    def test_get_channel_sub_count(self):
        url = self.channel_url
        self.yt.get(url)
        subs = None
        subs = self.yt.get_channel_sub_count()
        assert(subs != None)
        
    @unittest.skip("demonstrating skipping")
    def test_get_video_view_count(self):
        url = self.video_url
        self.yt.get(url)
        views =""
        views = self.yt.get_video_view_count()
        assert(type(views)==int)
        
    @unittest.skip("demonstrating skipping")
    def test_get_recent_videos_from_query(self):
        search_dict = self.yt.get_recent_videos_from_query('iceberg')
        assert(search_dict != {})
        
    # @unittest.skip("demonstrating skipping")
    def test_get_all_comments_from_video(self):
        import time
        url = self.video_url
        self.yt.get(url)
        time.sleep(1)
        comments={}
        comments = self.yt.get_all_comments_from_video()
        assert(comments!={})
        
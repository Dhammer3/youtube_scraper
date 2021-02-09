# An Easy to use Youtube Scraper

## Some Key Features Include:
* Collect Information on individual videos:
  - comments
  - likes 
  - dislikes
  - transcript
  - views
  - upload date
  - title
  - description
  - Subscribers
  
* Collect a list of videos on a YouTube channel
* Query a list of recently uploaded videos
* Basic text processing to store the information you want 
* Store this information in a .txt, csv, or HTML

* A WebDriver class written on top of the Selenium webdriver
  - find elements by xpath, tag, or ID and wait for them to load in
  
## Usage
### Setup
```python
webdriver = WebDriver()
yt = YoutubeCrawler(webdriver)
youtube_url = 'https://www.youtube.com/watch?v=rfscVS0vtbw&t=31s'
yt.get(youtube_url)
```
### Build a dataframe containing video information and transcript
``` python
yt.get_video_transcript()
```
### Get videos less than 5 weeks old from a query 
```python
video_dict = yt.get_recent_videos_from_query('awesome videos')
```
### Get all comments on a youtube video (first layer, non-recursive)
```python
comment_dictionary = yt.get_all_comments_from_video()
```
### Collect information on every video on a channel
```python
channel_url = "https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ"
yt.get_all_video_transcripts_from_channel(channel_url)
```
### Teardown
```python
del yt
```

### This code was intended to be used with a Jupyter notebook, so there is no main function.
### If this was helpful in any way, please star the repo :)

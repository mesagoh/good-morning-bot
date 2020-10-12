import tweepy
import urllib.request
import flickrapi
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import datetime
from photo import Photo
import time
import os
import xml
# xml.etree.ElementTree.dump(<XML_OBJ>)
from bs4 import BeautifulSoup
import config


CONSUMER_KEY = os.environ['twitter_cons_key']
CONSUMER_SECRET = os.environ['twitter_sec_key']
ACCESS_KEY = os.environ['twitter_acc_key']
ACCESS_SECRET = os.environ['twitter_acc_sec']
FLICKR_API_KEY = os.environ['flickr_api_key']
FLICKR_SECRET = os.environ['flickr_sec_key']

PHOTO_MESSAGE = 'Good Morning'
KEYWORD = 'morning'

# CONSUMER_KEY = config.twitter_cons_key
# CONSUMER_SECRET = config.twitter_sec_key
# ACCESS_KEY = config.twitter_acc_key
# ACCESS_SECRET = config.twitter_acc_sec
# FLICKR_API_KEY = config.flickr_api_key
# FLICKR_SECRET = config.flickr_sec_key

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter = tweepy.API(auth)  # twitter
flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_SECRET, cache=True) # flickr 
font_list=['AmaticSC-Bold.ttf', 'Caveat-Bold.ttf', 'Courgette-Regular.ttf',
            'DancingScript-Bold.ttf', 'Sacramento-Regular.ttf']

def get_photos():
    # 1. select an image
    photos = flickr.walk(text=KEYWORD,
                            privacy_filter=1,
                            tags=KEYWORD,
                            extras='url_c',
                            safe_search=1,
                            content_type=1,
                            has_geo=1,
                            per_page=100)
    photo_info = []
    for i, photo in enumerate(photos):
        uid = photo.get('owner')
        pid = photo.get('id')
        url = photo.get('url_c')
        title = photo.get('title')
        # info = flickr.photos.getInfo(photo_id=pid)
        # soup = BeautifulSoup(info.text, "lxml")
        # xml.etree.ElementTree.dump(flickr.photos.getInfo(photo_id=pid))
        # region = str(soup.find({'location'}).region.string)
        # print(soup.find("location"))
        # print(pid, title, region)

        p = Photo(uid, pid, url, title)
        photo_info.append(p)

        if i>1:
            break
    
    return photo_info

def prep_img(FONT_PATH):
    try:  
        img  = Image.open('./goodmorning.jpg')  
    except IOError: 
        pass

    # edit lighting
    contrastor = ImageEnhance.Contrast(img)
    img = contrastor.enhance(0.70)
    brightor = ImageEnhance.Brightness(img)
    img = brightor.enhance(1.30)

    width, height = img.size
    draw = ImageDraw.Draw(img)

    fontsize = 1  # starting font size
    img_fraction = 0.65 # portion of image width you want text width to be

    font = ImageFont.truetype(FONT_PATH, fontsize)
    while font.getsize(PHOTO_MESSAGE)[0] < img_fraction*img.size[0]:
        fontsize += 1
        font = ImageFont.truetype(FONT_PATH, fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(FONT_PATH, fontsize)

    draw.text((random.randint(10, int(width/3)), random.randint(10, int(height/2))), PHOTO_MESSAGE, fill=(255,255,255), font=font)
    img.save('./goodmorning_edit.jpg', quality=100)


def tweet_morning() :
    font = random.choice(font_list)
    FONT_PATH = './assets/' + font
    selected = random.choice(get_photos())
    cr_link = selected.photo_link()

    urllib.request.urlretrieve(selected.photo_url, 'goodmorning.jpg')
    prep_img(FONT_PATH) 

    # open editted img
    photo_file = open('goodmorning_edit.jpg','rb')
    photo_media = twitter.media_upload(filename='goodmorning_edit.jpg', file=photo_file)
    twitter.update_status('🌅 Good Morning! (source: '+cr_link+')', media_ids=[photo_media.media_id_string])

while True:
    now = datetime.datetime.now(datetime.timezone.utc)
    target_hour_PST = 14
    # pst       14
    # gmt+8     23
    if now.hour is target_hour_PST and now.minute is 0 and now.second is 0:
        tweet_morning()
    # if now.hour == 5 and now.minute == 51 and now.second == 0:
        # tweet_morning()
        # exit(0)




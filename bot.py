import tweepy
import urllib.request
import flickrapi
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import datetime
from photo import Photo
import time
import config

CONSUMER_KEY = config.twitter_cons_key
CONSUMER_SECRET = config.twitter_sec_key
ACCESS_KEY = config.twitter_acc_key
ACCESS_SECRET = config.twitter_acc_sec
FLICKR_API_KEY = config.flickr_api_key
FLICKR_SECRET = config.flickr_sec_key
PHOTO_MESSAGE = 'Good Morning'
KEYWORD = 'morning'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)  # twitter
flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_SECRET, cache=True) # flickr 
fontList=['AmaticSC-Bold.ttf', 'Caveat-Bold.ttf', 'Courgette-Regular.ttf',
            'DancingScript-Bold.ttf', 'Sacramento-Regular.ttf']

def tweetMorning() :
    fontSelected = random.choice(fontList)
    FONT_PATH = './assets/' + fontSelected

    # 1. select an image
    photos = flickr.walk(text=KEYWORD,
                            privacy_filter=1,
                            tags=KEYWORD,
                            extras='url_c',
                            safe_search=1,
                            content_type=1,
                            per_page=100)
    photoInfo = []
    for i, photo in enumerate(photos):
        user = photo.get('owner')
        phID = photo.get('id')
        url = photo.get('url_c')
        title = photo.get('title')
        

        p1 = Photo(user, phID, url, title)
        photoInfo.append(p1)

        if i>50:
            break

    selectedPhoto = random.choice(photoInfo)
    creditLink = 'https://www.flickr.com/photos/' + str(selectedPhoto.userID) + '/' + str(selectedPhoto.photoID)

    # 2. download image
    urllib.request.urlretrieve(selectedPhoto.photoUrl, 'goodmorning.jpg')

    # 3. open that image
    try:  
        img  = Image.open('./goodmorning.jpg')  
    except IOError: 
        pass

    # 4. edit lighting
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

    print(creditLink)

    # To get file object
    photoFile = open('goodmorning_edit.jpg','rb')
    photoMedia = api.media_upload(filename='goodmorning_edit.jpg', file=photoFile)
    api.update_status('🌅 Test Good Morning! [src 👉 ' + creditLink + ']', media_ids=[photoMedia.media_id_string])

while True:
    now = datetime.datetime.now(datetime.timezone.utc)
    targetHourPST = 14
    # pst       14
    # gmt+8     23
    if now.hour is targetHourPST and now.minute is 0 and now.second is 0:
        tweetMorning()




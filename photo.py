class Photo:
    def __init__(self, user_id, photo_id, photo_url, photo_title):
        self.user_id = user_id
        self.photo_id = photo_id
        self.photo_url = photo_url
        self.photo_title = photo_title

    def photo_link(self):
        return ('https://www.flickr.com/photos/' + str(self.user_id) + '/' + str(self.photo_id))
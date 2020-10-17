# Good Morning Twitter Bot
Do you send Good Morning pictures to greet your family group chats every morning? Save yourself some time and follow this project to share an auto-generated Good Morning photo with just one click! The [@GoodMorningPOTD](https://twitter.com/goodmorningpotd) bot tweets a Good Morning Photo everyday at 7AM PST. The project is hosted on Heroku. Uses [Flickr API](https://www.flickr.com/services/api/) and [Twitter API](https://developer.twitter.com/en/docs/twitter-api), and [Tweepy](https://www.tweepy.org/).

## Overview

1. Pick a random image with keyword from Flickr
2. Save the image as `goodmorning.jpg`
3. Open this saved image and enhance photo using Python Imaging Library. This is also the step where the text is added.
4. Save editted image as `goodmorning_edited.jpg`
5. When the time reaches, tweet this picture along with its source in a form of a link to the original Flickr page.

## Development
This basic bot will evolve into a more complex one with the ability to respond to Direct Messages for custom requests. For example, the user may want to customize the text they want to attach on the Good Morning Photo. It will also be able to tweet Good Morning photos according to the user's time zone!

## References
1) Tweepy Examples - https://github.com/tweepy/tweepy/tree/master/examples


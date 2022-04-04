from telnetlib import AUTHENTICATION
import matplotlib.pyplot as plt 
import tweepy
import re
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from os import path
from PIL import Image

# Twitter Authentication scripts
def authenticate(consumer_key, consumer_secret,access_token_key, access_token_secret):    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_user_tweeets(screen_name,api):
    alltweets = [] 
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    outtweets = [tweet.text for tweet in alltweets] 
    return outtweets

# making the wordcloud
def make_stopwords():
    text_file = open("all_stopwords.txt", "r")
    stopwords_list = text_file.read().split("\n")
    text_file.close()
    return set(stopwords_list)
  
def preprocess(out):
    text = " ".join(out)
    text = re.sub(pattern=r"http\S+",repl="",string=text.lower())
    text = re.sub(pattern=r"@\S+",repl="",string=text)
    return text

twitter_mask = np.array(Image.open("twitter.png"))


def make_wordcloud(st_words, out):
    text = preprocess(out)
    wordcloud = WordCloud(width=1800, height=900,stopwords=st_words,
                        max_font_size=250, max_words=400,
                        colormap='rainbow', collocations=True).generate(text)  

    image_colors = ImageColorGenerator(twitter_mask)

    fig = plt.figure(figsize=(20,10), facecolor='k')
    # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('twitter3.png', format="png")
    return fig
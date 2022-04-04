from telnetlib import AUTHENTICATION
import matplotlib.pyplot as plt 
import tweepy
import re
from wordcloud import WordCloud

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

def make_wordcloud(st_words, out):
    text = preprocess(out)
    wordcloud = WordCloud(width=1800, height=1200,stopwords=st_words,
                        max_font_size=250, max_words=100, background_color="white",
                        colormap='cool', collocations=True).generate(text)  

    fig = plt.figure(figsize=(18,12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig
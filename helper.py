from telnetlib import AUTHENTICATION
import matplotlib.pyplot as plt 
import tweepy
import sys
import os
import string
import re
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import pandas as pd
import nltk
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
nltk.download('vader_lexicon')
# from os import path
# from PIL import Image

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


def percentage(part, whole):
    return 100 * float(part)/float(whole)

def get_tweets(keyword, no_of_tweet, api):
    tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(no_of_tweet)
    return tweets

def preprocess_tweets(tweets):
    tweet_list = []
    for tweet in tweets:
        tweet_list.append(tweet.text)

    tweet_list = pd.DataFrame(tweet_list)
    tweet_list.drop_duplicates(inplace = True)
    tw_list = pd.DataFrame(tweet_list)
    remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
    rt = lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
    tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
    tw_list["text"] = tw_list.text.str.lower()
    #Calculating Negative, Positive, Neutral and Compound values

    tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
    for index, row in tw_list['text'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        if neg > pos:
            tw_list.loc[index, 'sentiment'] = "negative"
        elif pos > neg:
            tw_list.loc[index, 'sentiment'] = "positive"
        else:
            tw_list.loc[index, 'sentiment'] = "neutral"
        tw_list.loc[index, 'neg'] = neg
        tw_list.loc[index, 'neu'] = neu
        tw_list.loc[index, 'pos'] = pos
        tw_list.loc[index, 'compound'] = comp

    return tw_list




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

# twitter_mask = np.array(Image.open("twitter.png"))


# def make_wordcloud(st_words, out):
#     text = preprocess(out)
#     wordcloud = WordCloud(width=1800, height=900,stopwords=st_words,
#                         max_font_size=250, max_words=400,
#                         colormap='rainbow', collocations=True).generate(text)  

#     # image_colors = ImageColorGenerator(twitter_mask)

#     fig = plt.figure(figsize=(20,10), facecolor='k')
#     # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     return fig


# my functions

def percentage(part, whole):
    return 100 * float(part)/float(whole)


def preprocess_tweets(tweets):
    tweet_list = []
    for tweet in tweets:
        tweet_list.append(tweet.text)

    tweet_list = pd.DataFrame(tweet_list)
    tweet_list.drop_duplicates(inplace = True)
    tw_list = pd.DataFrame(tweet_list)
    tw_list["text"] = tw_list[0]
    
    remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
    rt = lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
    tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
    tw_list["text"] = tw_list.text.str.lower()
    #Calculating Negative, Positive, Neutral and Compound values

    tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
    for index, row in tw_list['text'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        if neg > pos:
            tw_list.loc[index, 'sentiment'] = "negative"
        elif pos > neg:
            tw_list.loc[index, 'sentiment'] = "positive"
        else:
            tw_list.loc[index, 'sentiment'] = "neutral"
        tw_list.loc[index, 'neg'] = neg
        tw_list.loc[index, 'neu'] = neu
        tw_list.loc[index, 'pos'] = pos
        tw_list.loc[index, 'compound'] = comp

    return tw_list

def get_tweets(keyword, no_of_tweet, api):
    tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(no_of_tweet)
    tw_list = preprocess_tweets(tweets)
    return tw_list

def count_values_in_column(data,feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])

def create_pie_chart(data, names):
    # Create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    plt.pie(data, labels=names)
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    return plt
    

def make_wordcloud(out):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width=1000, height=500,stopwords=stopwords,
                        max_font_size=250, max_words=100,repeat=True,
                        colormap='rainbow', collocations=True).generate(out)  

    # image_colors = ImageColorGenerator(twitter_mask)

    fig = plt.figure(figsize=(20,10), facecolor='k')
    # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig
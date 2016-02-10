#!/usr/bin/python
#Import the necessary methods from tweepy library
#the goal of this program is to obtain the number of tweets which include "streaming"
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import re
import time
from sys import stdout


#Variables that contains the user credentials to access Twitter API 
access_token = "3527076748-HflTXP74NjSWDIyuAmakc69VqTAZ29WIUVfdgjE"
access_token_secret = "XSKSRbfQ2baQFJ5Sc9WrSPf6AT05NvdpMtQi6fGLajEoR"
consumer_key = "X8B3WiESc1q6v8NQqRcP3kUvw"
consumer_secret = "Wb619BUbvSOTZ3Azoe1oYkCmVRE7yD3TkZMjFobDoi64XEcCLX"
#input kinds of secert key
def count_number(file):   #define the function that can count the number of sentences which contains 'streaming'
    tweets_data = []
    tweets_file = open(file, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)  #store all data
        except:
            continue
            time.sleep(2)
    tweets = pd.DataFrame()
    tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
    #extract the content from every tweet
    def if_word_in_text(word, text):
        word = word.lower()
        text = text.lower()
        same = re.search(word, text) #search if key word is in text
        if same:
            return True #if yes, return ture
        return False

    tweets['streaming'] = tweets['text'].apply(lambda tweet: if_word_in_text('streaming', tweet))
    #put all "streaming" into series
    
    m3=tweets['streaming'].value_counts()[True]
    # obtain the number of the sentences that include "streaming" exists.

    
    print "%d sentences include streaming"%m3
    stdout.flush()
    time.sleep(5)

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            savefile=open('data.csv','a')  #open file data.csv
            savefile.write(data)           
            savefile.write('\n') # store tweets in file
            savefile.close()
            count_number('data.csv')
            return True
        except:
            print 'error'
    def on_error(self, status):
        print status

#This handles Twitter authetification and the connection to Twitter Streaming API
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track=['streaming']) 
#This line filter Twitter Streams to capture data by the keywords: 'streaming'




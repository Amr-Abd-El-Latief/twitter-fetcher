import json
import csv
import tweepy
import re
#for sentaiment analysis
from textblob import TextBlob

"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""
def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase,filename_extension,tweets_count):
    
    # Default settings part
    if consumer_key == "":
        consumer_key = "put Default key here"

    if consumer_secret == "":
        consumer_secret = "put Default key here"

    if access_token == "":
        access_token = "put Default key here"

    if access_token_secret == "":
        access_token_secret = "put Default key here"



   
    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)
    #api = tweepy.API(auth, monitor_rate_limit=True, wait_on_rate_limit=True)
    #get the name of the spreadsheet we will write to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))
    fname = hashtag_phrase;
    print (fname)
    #open the spreadsheet we will write to
    #with open('%s.csv' % (fname), 'w') as file:
    with open('%s.csv' % (fname+'_'+filename_extension), 'w') as file: 
        w = csv.writer(file)

        #write header row to spreadsheet
        w.writerow(['timestamp','tweet_original_time', 'tweet_text', 'username', 'all_hashtags', 'followers_count','sentaiment_score'])
        loopCounter =0

        tweepyCursor = tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets', \
                                   lang="en", tweet_mode='extended',monitor_rate_limit=True,wait_on_rate_limit = True).items()
        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in tweepyCursor:
            try:

                print ("--------------------------------Start Of Tweet ---------------------------")
                loopCounter +=1
                print ("tweet number : " + str(loopCounter)) 
                #print (tweet)
                tweet_text =tweet.full_text.replace('\n',' ').encode('utf-8');
                #print(str(tweet.user));
                created_original_time =str(tweet.user.created_at)
                ##print ("--------------------------------------------------")
                ##print(created_original_time);
                analysis = TextBlob(tweet.full_text)
                print ("--------------------------------End Of Tweet ---------------------------")

                w.writerow([tweet.created_at,created_original_time, tweet_text, tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count,analysis.sentiment.polarity])
            except tweepy.TweepError:
                time.sleep(60 * 15)
                continue
            except tweepy.RateLimitError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break 
            
consumer_key = input('Consumer Key ')
consumer_secret = input('Consumer Secret ')
access_token = input('Access Token ')
access_token_secret = input('Access Token Secret ')
    
hashtag_phrase = input('Hashtag Phrase ')
filename_extension = input('File Name Extension :')
tweets_count = int(input('Number of Tweets to retrieve :'))



if __name__ == '__main__':
    search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase,filename_extension,tweets_count)

import pandas as pd
import tweepy
from textblob import TextBlob

auth = tweepy.OAuthHandler('XXXXXXXXX', 'XXXXXXXXXX')
auth.set_access_token('XXXXXXX', 'XXXXXXXXXXX')
api = tweepy.API(auth)

##trump_tweets = tweepy.Cursor(api.user_timeline, id = 'realDonaldTrump').items(1)
##for tweets in trump_tweets:
##    print(dir(tweets))

##Function to grab tweets
def grab_tweets(username):
##  search for trump tweets
    trump_tweets = tweepy.Cursor(api.user_timeline, id = username).items(100000)
##  create blank dataframe with fields I want
    tweets_df = pd.DataFrame(columns=('Date and Time', 'id', 'source', 'Geo', 'Place', 'Retweets', 'tweet', 'Sentiment Polarity'))
##  loop through tweets and save to tweets_df
    i = 1
    for tweet in trump_tweets:
##        print(dir(tweets))
        tweets_df.set_value(i,'id', tweet.id)
        tweets_df.set_value(i,'source', tweet.source)
        tweets_df.set_value(i,'tweet', tweet.text)
        tweets_df.set_value(i,'Geo', tweet.geo)
        tweets_df.set_value(i, 'Place', tweet.place)
        tweets_df.set_value(i, 'Favorites', tweet.favorite_count)
        tweets_df.set_value(i, 'Retweets', tweet.retweet_count)
        tweets_df.set_value(i, 'Date and Time', tweet.created_at)
        analysis = TextBlob(tweet.text)
        tweets_df.set_value(i, 'Sentiment Polarity', analysis.sentiment.polarity)
        i = i + 1
##    save tweets to CSV
    tweets_df.to_csv(username+'tweets.csv', encoding='utf-8')
##    print(tweets_df.head())
    
    
    
    
##Run function to grab tweets 
##grab_tweets('realDonaldTrump')

##save the count, rolling mean, and average daily sentiment polarity indexed by date for Quantopian
tweets_df = pd.DataFrame.from_csv('realDonaldTrumptweets.csv', encoding='utf-8')
tweets_df['Date'] = tweets_df['Date and Time'].str[:10]
print(tweets_df[tweets_df['Date']=='2017-01-23'])
data_df = tweets_df.groupby(['Date']).size().reset_index().rename(columns={0:'count'})
data_df.set_index('Date', inplace=True)
data_df['rolling mean'] = data_df['count'].rolling(window=10).mean()
data_df['Sentiment Polarity'] = tweets_df.groupby(['Date']).mean()['Sentiment Polarity']
data_df = data_df.shift(1)
data_df.to_csv('data.csv', encoding='utf-8')
print(data_df.tail())

##df = pd.DataFrame.from_csv('data.csv')
##df['rolling mean'] = df['count'].rolling(window=10).mean()
##print(df[10:15])
##print(df.tail())
##df = df.shift(1)
##print(df[10:15])
##print(df.tail())
##print(df.ix['2016-10-20', ['count']])
##print(df['count'].mean())

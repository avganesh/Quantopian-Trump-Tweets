# Quantopian-Trump-Tweets
Quantopian Algorithm using Trump Tweets data. 
First I use a tweepy cursor to grab a page of tweets by theRealDonaldTrump.
Then I score the sentiment of each tweet using textblob (shout out to TextBlob). 
Then I summarize daily counts of his tweets in a pandas DataFrame, 
calculate a 10-day rolling average count, 
and calculate the daily average sentiment score.
Finally I shifted the df by 1; yesterday's tweets will be today's data. 

I saved the data.csv file to dropbox, and used Quantopian's fetcher to grab the data. 
Then I tested a trading strategy based on the hypothesis that Trump's tweets with 
abs(polarity) > 0.2 will cause increased volatility in the market. 
To test the basic idea I just selected a VIX etf to trade +/- 100% of my portfolio. 

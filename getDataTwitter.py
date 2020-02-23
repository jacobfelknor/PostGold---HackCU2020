import tweepy
import re

from config.keys import twitter_client_id, twitter_client_secret, access_token, access_token_secret


def getTitleSentenceList(setOfTweets):
    titles = []
    my_title = []
    for status in setOfTweets:
        tweet = status._json
        newTweet = tweet["text"]
        if "RT @" not in newTweet and "http" not in newTweet:  # and ("https" not in tweet["text"]):
            my_title.append(newTweet)
            titles.append(my_title)
            my_title = []
    return titles


def getTitle(tweet):
    # continued from code above
    titleData = {}
    for title in tweet:
        title = title[0].lower()
        titles = re.sub("[^\w]", " ", title).split()
        for i in titles:
            if titleData.get(i, -1) == -1:
                titleData.update({i: 0})
            titleData[i] += 1
    print(titleData)


auth = tweepy.OAuthHandler(twitter_client_id, twitter_client_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

setOfTweets = api.user_timeline(screen_name="elonmusk", count=1000, include_rts=True)

getTitle(getTitleSentenceList(setOfTweets))

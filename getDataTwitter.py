import tweepy

from config.keys import twitter_client_id, twitter_client_secret, access_token, access_token_secret


def get_last_tweet(self):
    tweet = self.client.user_timeline(id=self.client_id, count=1)[0]
    print(tweet.text)


auth = tweepy.OAuthHandler(twitter_client_id, twitter_client_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

stuff = api.user_timeline(screen_name="kanyewest", count=200, include_rts=True)

for status in stuff:
    tweet = status._json
    if "RT @" not in tweet["text"]:  # and ("https" not in tweet["text"]):
        print(tweet["text"])


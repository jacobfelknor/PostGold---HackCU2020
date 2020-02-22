import praw
import string

from config.keys import client_id, client_secret, user_agent


def getTitle(reddit, subreddit, numberOfPosts):
    # continued from code above
    titleData = {}
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        title = submission.title
        title.translate(string.punctuation)
        titles = title.split(" ")
        for i in titles:
            if titleData.get(i, -1) == -1:
                titleData.update({i: 0})
            titleData[i] += 1
    print(titleData)


def getPostText(reddit, subreddit, numberOfPosts):
    textData = {}
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        text = submission.selftext
        text.translate(string.punctuation)
        posts = text.split(" ")
        for i in posts:
            if textData.get(i, -1) == -1:
                textData.update({i: 0})
            textData[i] += 1
    print(textData)


reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
subreddit = "lifeofnorman"
numberOfPosts = 50
getTitle(reddit, subreddit, numberOfPosts)
getPostText(reddit, subreddit, numberOfPosts)

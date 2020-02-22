import praw
import string
import re

from config.keys import client_id, client_secret, user_agent


def getTitle(reddit, subreddit, numberOfPosts):
    # continued from code above
    titleData = {}
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        title = submission.title
        title = title.lower()
        titles = re.sub("[^\w]", " ", title).split()
        for i in titles:
            if titleData.get(i, -1) == -1:
                titleData.update({i: 0})
            titleData[i] += 1
    print(titleData)

#gets list of title sentences 
def getTitleSentenceList(reddit, subreddit, numberOfPosts):
    titles = []
    my_title = []
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        #all the titles
        title = submission.title 
        # title = list(title)
        my_title.append(title)
        #print(my_title)
        titles.append(my_title)
        my_title = []
    print(titles)

#gets frequency per word
def getPostText(reddit, subreddit, numberOfPosts):
    textData = {}
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        #text is one long string
        text = submission.selftext
        text = text.lower()
        text = re.sub("[^\w]", " ", text).split()
        posts = text
        for i in posts:
            if textData.get(i, -1) == -1:
                textData.update({i: 0})
            textData[i] += 1
    print(textData)

#gets list of sentences where each sentence is a list 
def getPostSentenceList(reddit, subreddit, numberOfPosts):
    titles = []
    my_title = []
    my_string = ""
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        #all the titles
        title = submission.selftext
        for i in title:
            if i == '.' or i == '!' or i == '?':
                #print(my_string)
                my_title.append(my_string)
                #print(my_title)
                titles.append(my_title)
                my_title = []
                my_string = ""
            else:
                my_string += i
    print(titles)

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
subreddit = "lifeofnorman"
numberOfPosts = 50
#getTitleSentenceList(reddit, subreddit, numberOfPosts)
# getTitle(reddit, subreddit, numberOfPosts)
# print('--------------------------------------------------------------------------------')
# getPostText(reddit, subreddit, numberOfPosts)
getPostSentenceList(reddit, subreddit, numberOfPosts)
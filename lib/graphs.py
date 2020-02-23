import random
import re
import string

import networkx as nx
import praw
import tweepy

from config.keys import (
    access_token,
    access_token_secret,
    client_id,
    client_secret,
    twitter_client_id,
    twitter_client_secret,
    user_agent,
)


def getTweets(setOfTweets):
    tweets = []
    for status in setOfTweets:
        tweet = status._json
        newTweet = tweet["text"]
        if "RT @" not in newTweet and "http" not in newTweet:  # and ("https" not in tweet["text"]):
            tweets.append(newTweet.split())

    return tweets


def getTweetData(tweet):
    # continued from code above
    tweetData = {}
    for title in tweet:
        title = title[0].lower()
        titles = re.sub(r"[^\w]", " ", title).split()
        for i in titles:
            if tweetData.get(i, -1) == -1:
                tweetData.update({i: 0})
            tweetData[i] += 1
    return tweetData


def getTitle(reddit, subreddit, numberOfPosts):
    # continued from code above
    titleData = {}
    titleWords = []
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        title = submission.title
        title.translate(string.punctuation)
        titles = title.split(" ")
        titleWords.append(titles)
        for i in titles:
            if titleData.get(i, -1) == -1:
                titleData.update({i: 0})
            titleData[i] += 1
    return titleWords, titleData


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
    return textData


class Node:
    def __init__(self, *args, **kwargs):
        self.word = kwargs.pop("word", None)
        self.frequency = kwargs.pop("frequency", None)
        self.start = kwargs.pop("start", False)
        self.start_freq = kwargs.pop("start_freq", 0)
        self.end = kwargs.pop("end", False)
        self.end_freq = kwargs.pop("end_freq", 0)

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word


def search_graph(word, g):
    for node in g.nodes:
        if node.word == word:
            return node
    return None


def build_graph(titles, freqs, g):
    for title in titles:
        ii = 0
        last_node = None
        for word in title:
            first = False
            end = False
            if word == title[0]:
                # print(word)
                first = True
            elif word == title[-1]:
                end = True

            if not search_graph(word, g):
                freq = freqs.get(word, None)
                node = Node(word=word, frequency=freq, first=first, end=end)
                g.add_node(node)
                if first:
                    g.graph["firsts"].append(node)
                    node.start_freq += 1
                elif end:
                    g.graph["ends"].append(node)
                    node.end_freq += 1
            else:
                node = search_graph(word, g)
                if first:
                    g.graph["firsts"].append(node)
                    node.start_freq += 1
                elif end:
                    g.graph["ends"].append(node)
                    node.end_freq += 1

            if last_node:
                if g.has_edge(last_node, node):
                    g[last_node][node]["weight"] += 1
                else:
                    g.add_edge(last_node, node, weight=1)

            last_node = node

            ii += 1


def generate_title(g):
    gen_title = ""
    num_firsts = len(g.graph["firsts"])
    word = g.graph["firsts"][random.randrange(0, num_firsts)]

    while True:
        gen_title += word.word + " "
        len_edges = len(g.edges(word))
        if len_edges == 0:
            break
        l = list(g.edges(word, data=True))
        rn = []
        count = 0
        for x in l:
            new = [count] * (x[2]["weight"])
            rn += new
            count += 1
        x = random.randrange(0, len(rn))
        word = list(g.edges(word))[rn[x]][1]
        if word.end:
            if random.randrange(0, 1):
                break

    return gen_title


def get_sentences(subreddit):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    numberOfPosts = 300
    titles, freqs = getTitle(reddit, subreddit, numberOfPosts)
    # print(titles)
    g = nx.DiGraph(firsts=[], ends=[])

    build_graph(titles, freqs, g)

    ret = []
    seen = {}
    while len(ret) < 15:
        title = generate_title(g).strip()
        if not seen.get(title, None):
            ret.append(title)
            seen[title] = True
    return ret


def get_gen_tweets(handle):
    auth = tweepy.OAuthHandler(twitter_client_id, twitter_client_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    setOfTweets = api.user_timeline(screen_name=handle, count=5000, include_rts=True)

    tweets = getTweets(setOfTweets)
    # tweet_data = getTweetData(tweets)

    g = nx.DiGraph(firsts=[], ends=[])
    build_graph(tweets, {}, g)

    ret = []
    seen = {}
    while len(ret) < 15:
        gen_tweet = generate_title(g).strip()
        if not seen.get(gen_tweet, None):
            ret.append(gen_tweet)
            seen[gen_tweet] = True

    # print(ret)
    return ret

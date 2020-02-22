import random
import string

import networkx as nx
import praw

from config.keys import client_id, client_secret, user_agent


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
                node = Node(word=word, frequency=freqs[word], first=first, end=end)
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
                g.add_edge(last_node, node)

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
        word = list(g.edges(word))[random.randrange(0, len_edges)][1]
        if word.end:
            if random.randrange(0, 1):
                break

    return gen_title


if __name__ == "__main__":

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddit = "lifeofnorman"
    numberOfPosts = 300
    titles, freqs = getTitle(reddit, subreddit, numberOfPosts)
    # print(titles)
    g = nx.DiGraph(firsts=[], ends=[])

    build_graph(titles, freqs, g)
    # print(g.graph["ends"])
    # node = search_graph("in", g)
    # print(g.edges(node))
    for i in range(15):
        print(generate_title(g))
        print("\n\n")
    # print(list(g.edges(word))[0][])


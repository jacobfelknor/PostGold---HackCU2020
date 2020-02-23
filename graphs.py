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


def getTitleSentenceList(reddit, subreddit, numberOfPosts):
    titles = []
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        #all the titles
        title = submission.title 
        # title = list(title)
        title = title.lower()
        title = title.split(" ")
        #print(my_title)
        titles.append(title)
    return(titles)


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

def getPostSentenceList(reddit, subreddit, numberOfPosts):
    ret = []
    sentence = []
    word = ""
    for submission in reddit.subreddit(subreddit).top(limit=numberOfPosts):
        #all the titles
        contents = submission.selftext
        for i in contents:
            if i == '.' or i == '!' or i == '?':
                if word:
                    sentence.append(word)
                    word = ""
                if sentence:
                    ret.append(sentence)
                    sentence = []
            elif i.strip() == '':
                if word:
                    sentence.append(word)
                    word = ""
            else:
                if(i != '\n'):
                    word += i
    return ret




    #     for i in title:
    #         if i == '.' or i == '!' or i == '?' or i == '\n':
    #             #print(my_string)
    #             my_title.append(my_string)
    #             titles = my_title[0].split(" ")
    #             #print(my_title)
    #             titles.append(my_title)
    #             my_title = []
    #             my_string = ""
    #         else:
    #             my_string += i
    #     #titles = title.split(" ")
    
    # titles = [x for x in titles if x[0] != '']
    # for i in titles:
    #     if i[0] == '':
    #         print('\n')
    #         titles.remove(i)


class Node:
    def __init__(self, *args, **kwargs):
        self.word = kwargs.pop("word", None)
        #self.frequency = kwargs.pop("frequency", None)
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


def build_graph(titles, g):
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
                node = Node(word=word, first=first, end=end)
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
                if(g.has_edge(last_node, node)):
                    g[last_node][node]['weight'] += 1
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
        l = list(g.edges(word,data=True))
        rn = []
        count = 0
        for x in l:
            new = [count]*(x[2]['weight'])
            rn += new
            count += 1
        x = rn[random.randrange(0, len(rn))]
        #x = random.randrange(0, len_edges)
        word = list(g.edges(word))[x][1]
        if word.end:
            if random.randrange(0, 1):
                break

    return gen_title


if __name__ == "__main__":

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    subreddit = "amitheasshole"
    numberOfPosts = 500
    titles2 = getTitleSentenceList(reddit, subreddit, numberOfPosts)

    # bodies = getPostSentenceList(reddit, subreddit, numberOfPosts)

    # gB = nx.DiGraph(firsts=[], ends=[])

    # build_graph(bodies, gB)

    gT = nx.DiGraph(firsts=[], ends=[])

    build_graph(titles2, gT)

    for i in range(15):
        print(generate_title(gT))
        print("\n\n")
    # for i in range(5):
    #     print(generate_title(gB))
    #     print('\n\n **wait** \n\n')


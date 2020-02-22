import praw

from config.keys import client_id, client_secret, user_agent

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
print(reddit.read_only)  # Output: True

# continued from code above

for submission in reddit.subreddit("learnpython").hot(limit=10):
    print("TITLE: ", submission.title)
    print("CONTENT: ", submission.selftext)

# Output: 10 submissions

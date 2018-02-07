import praw

# Make your own profile file with all these variables for oauth 2
from profile import CLIENT_ID
from profile import CLIENT_SECRET
from profile import PASSWORD
from profile import USERAGENT
from profile import USERNAME

r = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, password = PASSWORD,
                user_agent = USERAGENT, username = USERNAME)


def get_sub_count():
    subreddits = open('subreddits.txt')
    for line in subreddits:
        line = line.rstrip('\n')
        sc = r.subreddit(line).subscribers
        print(line + ": " + str(sc))
        # try:
        #     sc = r.subreddit(line).subscribers
        #     print(line + ": " + str(sc))
        # except:
        #     print(line)


get_sub_count()

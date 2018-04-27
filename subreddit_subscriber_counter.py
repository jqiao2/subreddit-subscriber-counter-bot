from datetime import datetime

import pandas as pd
import praw

# Make your own profile file with all these variables for oauth 2
from profile import CLIENT_ID
from profile import CLIENT_SECRET
from profile import PASSWORD
from profile import USERAGENT
from profile import USERNAME

# Non-porn NSFW subreddits, add more if you want
BLACKLISTED_SUBREDDITS = ['ImGoingToHellForThis', 'FiftyFifty', 'MorbidReality',
                          'watchpeopledie', 'DarkNetMarkets', 'gore', 'AskRedditAfterDark',
                          'DarkNetMarketsNoobs']
# Add any strings you don't want the subreddit names to contain
FILTERS = ['gone', 'gw', 'hentai', 'wife', 'cest']
# Won't process any subreddits with fewer than SUBSCRIBER_THRESHOLD subscribers
SUBSCRIBER_THRESHOLD = 50000
# Reddit agent
r = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, password=PASSWORD,
                user_agent=USERAGENT, username=USERNAME)


def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)


time = str(datetime.now())
subreddits = r.subreddits.popular(limit=2000000)

subreddit_list = []
i = 0
while True:
    try:
        subreddit = subreddits.next()
    except StopIteration:
        break

    # filtered = not any([(filter_ in subreddit.display_name.lower()) for filter_ in
    #                     FILTERS]) and subreddit.display_name not in BLACKLISTED_SUBREDDITS
    filtered = subreddit.display_name not in BLACKLISTED_SUBREDDITS
    if subreddit.over18 and filtered and subreddit.subscribers > 50000:
        subreddit._fetch()
        submission_scores = []
        for submission in subreddit.top('year', limit=100):
            submission_scores.append(submission.score)
        average_score = mean(submission_scores)
        row = {"Subreddit": subreddit.display_name, "Subscribers": subreddit.subscribers,
               "Active Accounts": subreddit.accounts_active, "Average Score": average_score}
        subreddit_list.append(row)
        print("Processed", subreddit)

pd.DataFrame(
    subreddit_list, columns=["Subreddit", "Subscribers", "Active Accounts", "Average Score"]
).to_csv(time + " subreddits.csv")
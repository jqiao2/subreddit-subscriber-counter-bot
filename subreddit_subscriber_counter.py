import pandas as pd
import praw

# Make your own profile file with all these variables for oauth 2
from profile import CLIENT_ID
from profile import CLIENT_SECRET
from profile import PASSWORD
from profile import USERAGENT
from profile import USERNAME

# Reads subreddit names from a .txt file and creates a .csv file with subreddit names
# and subscriber count.

r = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, password=PASSWORD,
                user_agent=USERAGENT, username=USERNAME)


def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)


# Non-porn or non- subreddits
blacklisted_subreddits = ['ImGoingToHellForThis', 'FiftyFifty', 'MorbidReality',
                          'watchpeopledie', 'DarkNetMarkets', 'gore', 'AskRedditAfterDark',
                          'NSFWFunny', 'MassiveCock', 'Overwatch_Porn', 'futanari', 'rule34']
filters = ['gone', 'gw', 'hentai', 'wife', 'cest']

subreddit_list = []
subreddits = r.subreddits.popular(limit=2000000)
for _ in range(20000):
    subreddit = subreddits.next()
    filtered = not any([(filter_ in subreddit.display_name.lower()) for filter_ in
                        filters]) and subreddit.display_name not in blacklisted_subreddits
    if subreddit.over18 and filtered:
        subreddit._fetch()

        submission_scores = []
        for submission in subreddit.top('year', limit=100):
            submission_scores.append(submission.score)
        average_score = mean(submission_scores)

        row = {"Subreddit": subreddit.display_name, "Subscribers": subreddit.subscribers,
               "Active Accounts": subreddit.accounts_active, "Average Score": average_score}
        subreddit_list.append(row)
        print("Processed", subreddit)

subreddit_data_frame = pd.DataFrame(subreddit_list, columns=["Subreddit", "Subscribers",
                                                             "Active Accounts", "Average Score"])
subreddit_data_frame.to_csv("subreddits.csv")

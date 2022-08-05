import praw

with open('SECRET') as f:
	reddit = eval(f.read())

submissions = reddit.subreddit("dadjokes").top(time_filter='day',
                                         limit=10)
for p in submissions:
	print(p.title)
	print(p.selftext)
	print()
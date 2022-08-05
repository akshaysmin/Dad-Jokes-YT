import praw
import csv
from datetime import datetime
import re

###CONSTANTS###
regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
MAX_JOKES = 10

###FUNCTIONS###
def is_joke_valid(jk):
	if_no_links = len(re.findall(regex, jk))==0
	return if_no_links

with open('SECRET') as f:
	reddit = eval(f.read())

valid_jokes = 0
ids = []

while valid_jokes<MAX_JOKES:
	submissions = reddit.subreddit("dadjokes").top(time_filter='day',
                                                       limit=2*MAX_JOKES-valid_jokes+1)
	#input('hehe')
	with open('dadjokes.csv', 'a', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',)
		for p in submissions:
			title = p.title
			text = p.selftext
			id = p.id
			
			#speedbreaker
			if  valid_jokes==MAX_JOKES:
				break
			elif (id in ids):
				continue
			elif is_joke_valid(title+text):
				valid_jokes += 1
			else:
				continue

			ids.append(id)
			time = p.created
			timestamp =  datetime.fromtimestamp(time).strftime("%Y/%m/%d, %H:%M:%S")
			print(valid_jokes)
			print(id)
			print(text)
			writer.writerow([p.id, p.author, timestamp, p.url, p.title, p.selftext])
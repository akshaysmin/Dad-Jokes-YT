import praw
import csv
from datetime import datetime
import re

###CONSTANTS###
regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
MAX_JOKES = 10
MAX_ITER = 10
MAX_SENTENCES = 9

###FUNCTIONS###
def is_joke_valid(jk, id):
	sentences = [s if len(s)>1 for s in jk.split('.')]
	if_no_links = len(re.findall(regex, jk))==0
	if_new_joke = id not in old_jokes
	if_not_lengthy = len(sentences)<=MAX_SENTENCES
	print(if_new_joke)
	return if_no_links and if_new_joke

with open('SECRET') as f:
	reddit = eval(f.read())

#get id of old jokes
old_jokes = []
with open('dadjokes.csv') as f:
	reader = csv.reader(f)
	next(reader) #skips header
	for row in reader:
		old_jokes.append(row[0])

def main():
	valid_jokes = 0
	ids = []
	iter = 0
	while valid_jokes<MAX_JOKES and iter<MAX_ITER:
		iter += 1
		submissions = reddit.subreddit("dadjokes").top(time_filter='day',
	                                                       limit=iter*MAX_JOKES)
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
				elif is_joke_valid(title+text, id):
					valid_jokes += 1
				else:
					continue
	
				time = p.created
				timestamp =  datetime.fromtimestamp(time).strftime("%Y/%m/%d, %H:%M:%S")
				print(valid_jokes)
				print(id)
				print(title)
				print(text)

				#save joke
				try :
					writer.writerow([id, p.author, timestamp, p.url, title, text])
				except UnicodeEncodeError as err:
					valid_jokes -= 1
					print(err, 'Handled')
					continue

				ids.append(id)
				print('NICE ONE')

main()
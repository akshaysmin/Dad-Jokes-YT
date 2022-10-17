from dadscraper import scrape_jokes
from video_maker import make_video
from uploader import upload_video

scrape_jokes()
make_video()

options = {'--file': 'joke10.mp4',
           '--title': 'Dad Jokes that Make you Laugh',
           '--description': 'Jokes from r/dadjokes',
           '--keywords': 'jokes,joke,reddit,dad jokes,dad,funny,laugh,lol',
           '--privacyStatus': 'public',  # ("public", "private", "unlisted")
           # '--categoryId':'',
           }

upload_video(options=options)

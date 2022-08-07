import moviepy.editor as mpy
import numpy as np
import cv2
import matplotlib.pyplot as plt
import csv

class GetFrame:
	def __init__(self, frames):
		self.frames = frames

	def __call__(self, x):
		print(f'recieved {x}')
		return self.frames[0]

def load_joke10():
	joke10 = []
	with open('joke10.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			joke = (row[4],row[5])
			joke10.append(joke)
			next(reader)
	return joke10
	

def main():
	path = 'blue_dark_cloud.jpg'
	background = cv2.imread(path)
	background = cv2.cvtColor(background , cv2.COLOR_BGR2RGB)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	org = (50, 50)
	fontScale = 1
	color = (255, 0, 0)
	thickness = 2
	
	joke10 = load_joke10()
	text = ''
	frames = []
	for jk in joke10:
		text += jk[0] + '\n' + jk[1]
	
		image = cv2.putText(background , text, org, font, fontScale, color, thickness, cv2.LINE_AA)
		np_img = np.asarray(image)
		frames.append(np_img)
	
	get_frame = GetFrame(frames)
	mpy.VideoClip(get_frame, duration=10).write_videofile('test.mp4', fps=12)

main()
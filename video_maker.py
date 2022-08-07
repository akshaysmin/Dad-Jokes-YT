import moviepy.editor as mpy
import numpy as np
import cv2
import matplotlib.pyplot as plt
import csv
import textwrap

###CONSTANTS##
DURATION = 10
BACKGROUND_IMG = 'blue_dark_cloud.jpg'



###FUNCTIONS###

class GetFrame:
	def __init__(self, frames, frame_rate = None, duration=None):
		self.frames = frames
		self.duration = duration
		if frame_rate is not None:
			self.frame_rate = frame_rate
		elif duration is not None:
			self.frame_rate = len(frames)//duration

	def __call__(self, x):
		try:
			return self.frames[int(self.frame_rate*x)]
		except IndexError as err:
			return self.frames[-1]

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
	global background, npimg, joke10, frames, text, wrapped_text
	global font, org, font_size, font_color, font_thickness
	
	path = BACKGROUND_IMG
	background = cv2.imread(path)
	background = cv2.cvtColor(background , cv2.COLOR_BGR2RGB)
	height, width, channel = background.shape
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	org = (50, 50)
	font_size = 1
	font_color = (255, 255, 255)
	font_thickness = 2
	
	joke10 = load_joke10()
	frames = []
	for i,jk in enumerate(joke10):

		text = str(i) + '\n' + jk[0] + '\n' + jk[1]
		textsize = cv2.getTextSize('O', font, font_size, font_thickness)[0]
		gap = textsize[1] + 10
		wrapped_text = textwrap.wrap(text, width=width//textsize[0])

		image = background.copy()

		for i, line in enumerate(wrapped_text):
			textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
			y = (height - textsize[1]) // 2 + i * gap
			x = (width - textsize[0])//2
			org = (x,y)
			image = cv2.putText( image , line, org, font, font_size, font_color, font_thickness, cv2.LINE_AA)

		plt.imshow(image)
		plt.show()
#		cv2.imshow('hehe', image)
#		cv2.waitKey(0)
		np_img = np.asarray(image)
		frames.append(np_img)

	get_frame = GetFrame(frames, duration = DURATION)
	mpy.VideoClip(get_frame, duration=DURATION).write_videofile('test.mp4', fps=12)

main()
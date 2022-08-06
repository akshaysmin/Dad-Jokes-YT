import moviepy.editor as mpy
import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_frame(x):
	return img

path = 'blue_dark_cloud.jpg'
image = cv2.imread(path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2

image = cv2.putText(image, 'OpenCV', org, font, fontScale, color, thickness, cv2.LINE_AA)
img = np.asarray(image)

mpy.VideoClip(get_frame, duration=10).write_videofile('test.mp4', fps=12)

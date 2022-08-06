import moviepy.editor as mpy
from PIL import Image
import numpy as np

def get_frame(x):
	return img

p = Image.open('Dark_mode_image.jpg')
img = np.asarray(p)

mpy.VideoClip(get_frame, duration=10).write_videofile('test.mp4', fps=12)

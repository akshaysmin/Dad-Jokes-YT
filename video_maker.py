import moviepy.editor as mpy
import numpy as np
import cv2
import matplotlib.pyplot as plt
import csv
import textwrap

from audio_maker import tell_jokes
import tempfile

###CONSTANTS##
DURATION = 60
BACKGROUND_IMG = 'blue_dark_cloud.jpg'
mpy.AudioClip

###FUNCTIONS###


class GetFrame:
    def __init__(self, frames, durations=None, frame_rate=None, duration=None):
        self.frames = frames
        self.duration = duration
        if durations is not None:
            self.durations = durations
        elif frame_rate is not None:
            self.frame_rate = frame_rate
        elif duration is not None:
            self.frame_rate = len(frames)/duration

    def __call__(self, x):
        try:
            if self.durations:
                if x > sum(self.durations):
                    raise IndexError
                lower = 0
                cum = 0
                for i, dur in enumerate(self.durations):
                    cum += dur
                    if cum > x:
                        upper = cum
                        break
                    elif cum < x:
                        lower = cum

                frame = self.frames[i]
            else:
                frame = self.frames[int(self.frame_rate*x)]
        except IndexError as err:
            return self.frames[-1]

        return frame


def load_joke10():
    joke10 = []
    with open('joke10.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            joke = (row[4], row[5])
            joke10.append(joke)
            next(reader)
    return joke10


def get_audio(joke10_plus):
    print('making speech')
    told_jokes, synthesizer = tell_jokes(joke10_plus)

    speeches = []
    for wav in told_jokes:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            # todo : find a way to not persist tempfile
            synthesizer.save_wav(wav, fp)
            speeches.append(fp.name)
    told_jokes = speeches

    print(told_jokes)

    audioclips = [mpy.AudioFileClip(i) for i in told_jokes]
    audioclip = mpy.concatenate_audioclips(audioclips)
    durations = [clip.duration for clip in audioclips]

    return audioclip, durations


def get_video(durations):
    global background, npimg, joke10, frames, text, wrapped_text
    global font, org, font_size, font_color, font_thickness

    path = BACKGROUND_IMG
    background = cv2.imread(path)
    background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
    height, width, channel = background.shape

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    font_size = 1
    font_color = (255, 255, 255)
    font_thickness = 2

    frames = []
    for i, jk in enumerate(joke10):

        text = str(i) + '\n' + jk[0] + '\n' + jk[1]
        textsize = cv2.getTextSize('O', font, font_size, font_thickness)[0]
        gap = textsize[1] + 10
        wrapped_text = textwrap.wrap(text, width=width//textsize[0])

        image = background.copy()

        for i, line in enumerate(wrapped_text):
            textsize = cv2.getTextSize(
                line, font, font_size, font_thickness)[0]
            y = (height - textsize[1]) // 2 + i * gap
            x = (width - textsize[0])//2
            org = (x, y)
            image = cv2.putText(image, line, org, font, font_size,
                                font_color, font_thickness, cv2.LINE_AA)

        np_img = np.asarray(image)
        frames.append(np_img)

    get_frame = GetFrame(frames, durations=durations)
    clip = mpy.VideoClip(get_frame, duration=sum(durations))
    return clip


def make_video():
    joke10_plus = [i + ' ' + j for i, j in joke10]

    audioclip, durations = get_audio(joke10_plus)
    videoclip = get_video(durations)

    videoclip.audio = audioclip
    videoclip.write_videofile('joke10.mp4', fps=12)


joke10 = load_joke10()

if __name__ == '__main__':
    make_video()

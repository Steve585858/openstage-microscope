#https://www.makeartwithpython.com/blog/creating-slit-scan-images-in-python-and-moviepy/
#pip install Pillow, moviepy

from moviepy.editor import VideoFileClip
import numpy as np

from PIL import Image

class Scan():
    def __init__(self, iType, inputFileName, outputFileName):
        super().__init__()
        self.iType=iType  
        self.inputFileName=inputFileName
        self.outputFileName=outputFileName

    def getMovieInfo(self):
        clip = VideoFileClip(self.inputFileName)
        print('%s is %i fps, for %i seconds at %s' % (self.inputFileName, clip.fps, clip.duration, clip.size))

        clip = clip.subclip(20, 30)
        print('clip is %i fps, for %i seconds at %s' % (clip.fps, clip.duration, clip.size))
        #clip.write_videofile(self.outputFileName)
        #clip.write_gif(self.outputFileName) 
 
        # showing clip
        #clip.ipython_display()

    def movieClipToImage(self):
        clip = VideoFileClip(self.inputFileName)
        print('%s is %i fps, for %i seconds at %s' % (self.inputFileName, clip.fps, clip.duration, clip.size))
        clip = clip.subclip(20, 30)
        print('subclip is %i fps, for %i seconds at %s' % (clip.fps, clip.duration, clip.size))

        # np.zeros is how we generate an empty ndarray
        img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')

        currentX = 0
        slitwidth = 1

        slitpoint = clip.size[0] // 2

        # generate our target fps with width / duration
        target_fps = clip.size[0] / clip.duration

        for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
            if currentX < (clip.size[0] - slitwidth):
                img[:,currentX:currentX + slitwidth,:] = i[:,slitpoint:slitpoint+slitwidth,:]
            currentX += slitwidth

        output = Image.fromarray(img)
        output.save(self.outputFileName)

    def gifClip(self):
        clip = VideoFileClip(self.inputFileName).resize(0.2)
        print('%s is %i fps, for %i seconds at %s' % (self.inputFileName, clip.fps, clip.duration, clip.size))

        # np.zeros is how we generate an empty ndarray
        img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')

        currentX = 0
        slitwidth = 1

        slitpoint = clip.size[0] // 2

        frame_generator = clip.iter_frames(fps=clip.fps, dtype='uint8')

        # generate our target fps with width / duration
        target_fps = clip.size[0] / clip.duration

        for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
            if currentX < (clip.size[0] - slitwidth):
                img[:,currentX:currentX + slitwidth,:] = i[:,slitpoint:slitpoint+slitwidth,:]
            currentX += slitwidth

        
        output = VideoClip(make_frame=self.make_frame, duration=10.5)
        output.write_gif('output1.gif', fps=12)

    def make_frame(self, t):
        global img, currentX
        next_frame = next(frame_generator)
        img = np.roll(img, -1, axis=0)
        img[slitpoint,:,:] = next_frame[slitpoint,:,:]
        next_frame[max(slitpoint - currentX, 0):slitpoint,:,:] = img[max(0, slitpoint - currentX):slitpoint,:,:]
        currentX += 1
        return next_frame
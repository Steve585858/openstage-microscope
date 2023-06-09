
import time
import datetime
import os
from pathlib import Path

from Scan import Scan


root = Path(os.path.abspath(__file__)).parents[0]
path_parent = Path(os.path.abspath(__file__)).parents[1]
data_path = os.path.join(path_parent, 'examples')

def testScan():
    iType = 0
    inputFileName = os.path.join(data_path, 'spidermanTrailer-720p.mp4')
    outputFileName = os.path.join(data_path, 'spidermanTrailer-720p.jpg')
    scan = Scan(iType, inputFileName, outputFileName)
    #scan.getMovieInfo()
    scan.movieClipToImage()

def youtubeDownloader():
    outputFileName = os.path.join(data_path, 'smoothZ10.jpg')
    #https://github.com/opensciencegrid/BLAH/blob/1d217fad9c6b54a5e543f7a9d050e77047be0bb1/src/scripts/pbs_submit.sh#L193
    #https://thegrayarea.tech/5-python-automation-scripts-i-use-every-day-74c4313f2b47
    #https://thinkinfi.com/download-youtube-videos-in-python-with-pytube/

    from pytube import YouTube
    #link = input("Enter a youtube video's URL") # i.e. https://youtu.be/dQw4w9WgXcQ
    #link = 'https://www.youtube.com/watch?v=cU2bBZbU80I'
    link = 'https://www.youtube.com/watch?v=shW9i6k8cB0'

    yt = YouTube(link)
    #print(yt.streams)
    check = 0
    if check==1:
        preffered_resolution = ['144p', '240p', '360p', '480p', '720p', '1080p']
        for resolution in preffered_resolution:
            video_streams = yt.streams.filter(progressive=True, res=resolution)
            if len(video_streams) > 0:
                print(resolution)
            else:
                print(resolution + ' Audio is not available')
    else:
        yt.streams.filter(res="480p").first().download(data_path, 'spidermanTrailer.mp4')
        #yt.streams.first().download()
        print("downloaded", link)

def testController():
    outputFileName = os.path.join(data_path, 'smoothZ10.jpg')

    
def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()
    ct = datetime.datetime.now()
    print("PROCESSING...")
    print("current time:-", ct)

    testScan()
    #youtubeDownloader()

    end_time = time.time()
    seconds = end_time - start_time
    print("time of execution = {} seconds or hh:mm:ss {} ".format(seconds, format_seconds_to_hhmmss(seconds)))
    ct = datetime.datetime.now()
    print("current time:-", ct)
from pytube import YouTube
import os
from random import randint
import subprocess
import re


async def download(search):
    global audiofile
    global audiolength
    global audioname
    os.chdir(os.getcwd() + "/tmp")
    yt = YouTube(search)

    video = yt.streams.filter(only_audio=True).first()

    out_file = video.download(output_path=".")

    audiofile = str(randint(1,10000)) + '.mp3'
    os.rename(out_file, audiofile)
    args=("ffprobe","-show_entries", "format=duration","-i",audiofile)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    audiolength = int(round(float(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",str(popen.stdout.read()))[0])))
    os.chdir("..")
    out_file = out_file.replace("/home/pi/homedepotbot/tmp/./","").replace(".mp3","").replace(".mp4","")
    print(out_file)
    audioname = out_file
    return audioname
    return audiofile
    return audiolength

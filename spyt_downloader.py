import json
from datetime import datetime
import os
from os.path import isfile
import pytube


class spyt_downloader:

    def __init__(self, urls_file):
        self.URLs = json.loads(urls_file)
        self.downloads = []
        self.download_time = 0

    def download(self, directory):

        # start time tracking
        self.download_time = datetime.now()

        # check download directory
        if directory[-4:] != ".mp3" and not os.path.exists(directory):
            os.mkdir(directory)

            # ensure directory ends with "/", for usage later
            if directory[len(directory) - 1] != "/":
                directory += "/"

        elif directory[-4:] == ".mp3":
            directory = ""

        # start downloading videos
        for k in self.URLs.keys():

            # if already exists skip
            if isfile(directory + k + ".mp3"):
                continue

            # initialize pytube
            YT = pytube.YouTube(self.URLs[k][0] if isinstance(self.URLs[k], list) else self.URLs[k])

            # try downloading video from stream
            try:
                self.downloads.append(YT.streams.filter(only_audio=True).get_audio_only().download(directory + k + ".mp3"))
            except:
                self.downloads.append("error")

        # finish time tracking
        self.download_time = datetime.now() - self.download_time



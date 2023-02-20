from spt_searcher import spt_searcher
from youtubesearchpython import Playlist
import json


class ytb_searcher(spt_searcher):

    def __init__(self, *args, **kwargs):
        super(ytb_searcher, self).__init__(*args, **kwargs)
        self.key = args[0]
        self.ytURLS = {}

    def parse(self):
        try:
            some_object_iterator = iter(self.ytURLS)
        except TypeError:
            self.find_tracks()

    def find_yt_tracks(self, file=False):
        playlist = Playlist.getVideos(self.key)
        for xi in playlist["videos"]:
            if xi["isPlayable"]:
                t = xi["title"].replace('"', '').replace("''", "")
                self.ytURLS[t] = xi["link"].split('&list').pop(0)



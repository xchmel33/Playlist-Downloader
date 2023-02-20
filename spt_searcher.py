import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
from youtubesearchpython import VideosSearch


class spt_searcher:
    """
    Spotify playlist and it's tracks urls searcher class
    """

    def __init__(self, link, client_id="", client_secret=""):
        self.key = link.split("/").pop().split("?").pop(0)
        self.clientID = client_id
        self.clientSECRET = client_secret
        self.playlist_name = "Unknown"
        self.tracks = []
        self.ytURLS = {}
        self.yt404s = []
        self.ytSearches = 0
        self.time = 0

    def find_sp_tracks(self, file=False):

        # start time tracking
        self.time = datetime.now()

        # Create instance for using spotipy library API
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=self.clientID, client_secret=self.clientSECRET))

        # Get playlist's tracks
        results = sp.playlist_items(self.key)

        # Get and save playlist's name
        self.playlist_name = sp.playlist(playlist_id=self.key, fields="name")['name']

        # Optional - save playlists data
        if file:
            f = open(file, "w")
            json.dump(results, f, indent=4)

        # Save playlists's tracks with artist name
        for item in results['items']:
            self.tracks.append(item['track']['name'] + " - " + item["track"]["artists"][0]["name"])

        # Search for Youtube video URLS and save them
        for query in self.tracks:
            query = str.replace(query, " ", "%")
            try:
                self.__find_ytURL(query)
            except False:
                print("Error search video")

        # finish time tracking
        self.time = datetime.now() - self.time

    def __ytSearch(self, query, name):
        videosSearch = VideosSearch(query, limit=2)
        try:
            self.ytURLS[name] = videosSearch.result()["result"][1]["link"]
        except TypeError as te:
            self.yt404s.append(te)

    def __find_ytURL(self, query):

        # try to find link in file with already saved links
        f = open("search_links.json", "r")
        name = str.replace(query, "%", "_")
        jsn = json.loads(f.read())
        try:
            self.ytURLS[name] = jsn[query]

        # search for Youtube video link
        except KeyError:
            self.ytSearches += 1
            self.__ytSearch(query, name)
            self.write_to_json(name)

    def write_to_json(self, name, filename='search_links.json'):
        """
        Function that adds track's Youtube links to JSON
        ---------------------------------------------------------
        :param name: track's name
        :param new_data: track's Youtube URL
        :param filename: name of JSON file containing track links
        ---------------------------------------------------------
        """

        with open(filename, 'r+') as file:

            # First we load existing data into a dict.
            file_data = json.load(file)

            # Join new_data with file_data inside emp_details
            file_data[name] = self.ytURLS[name]

            # Sets file's current position at offset.
            file.seek(0)

            # convert back to json.
            json.dump(file_data, file, indent=4)

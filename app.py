from flask import Flask, request, jsonify
from flask_cors import CORS
from spt_searcher import spt_searcher
from ytb_searcher import ytb_searcher
from spyt_downloader import spyt_downloader
import shutil

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def goto_hell():
    return "GO TO HELL!"


@app.route('/spotify', methods=['POST'])
def find_sp_tracks():
    data = request.form
    spt = spt_searcher(data['playlist_link'], data['client_id'], data['client_secret'])
    spt.find_sp_tracks()
    return str(spt.ytURLS)
    # return "test"


@app.route('/youtube', methods=["POST"])
def find_yt_tracks():
    data = request.form
    ytb = ytb_searcher(data['playlist_link'])
    ytb.find_yt_tracks()
    return str(ytb.ytURLS)


@app.route('/download', methods=['POST'])
def download_all():
    data = request.form
    downloader = spyt_downloader(data['urls'])
    downloader.download(data['playlist_name'])
    shutil.make_archive(data['playlist_name'], 'zip', data['playlist_name'])
    return data['playlist_name']+'.zip' if data['playlist_name'][-4:] != ".mp3" else data['playlist_name']

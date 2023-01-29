from urllib.parse import urlencode
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

from util import randomstr, generate

import base64
import os
import requests

# load from env file
load_dotenv()

# initialize app
app = Flask(__name__)

# auto-reload templates in dev env
app.config["TEMPLATES_AUTO_RELOAD"] = True

# responses not cached
# @app.after_request
# def after_request(response):
   # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
   # response.headers["Expires"] = 0
   # response.headers["Pragma"] = "no-cache"
   # return response

# config session settings
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# api urls
authurl = 'https://accounts.spotify.com/authorize?'
tokenurl = 'https://accounts.spotify.com/api/token?'
requrl = 'https://api.spotify.com/v1/'

# initial auth parameters
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://127.0.0.1:5000/callback/'
SCOPES = 'user-read-currently-playing user-read-playback-state user-top-read user-read-currently-playing user-read-email'
STATE = randomstr(16)

# dict of init params for url generation
authparams = {
    'response_type': 'code',
    'client_id': CLIENT_ID,
    'scope': SCOPES,
    'show_dialog': True,
    'state': STATE
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/auth")
def auth():
    url = urlencode(authparams)
    loginurl = authurl + url + f"&redirect_uri={REDIRECT_URI}"
    return redirect(loginurl)


@app.route("/callback/", methods=["GET", "POST"])
def callback():

    if request.args.get("error") != None:
        return render_template("error.html")

    session["code"] = request.args.get("code")
    encids = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())

    accessparams = {
        'code': str(session["code"]),
        'grant_type': "authorization_code",
        'redirect_uri': REDIRECT_URI
    }

    session['accessheaders'] = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization':  "Basic {}".format(encids.decode())
    }

    response = requests.post(tokenurl, data=accessparams, headers=session['accessheaders'])
    data = response.json()

    # access_token, token_type, scope, expires_in, refresh_token
    session['access_token'] = data["access_token"]
    session['refresh_token'] = data["refresh_token"]

    session['auth_header'] = {
    'Authorization': f'Bearer {session["access_token"]}',
    'CONTENT-TYPE': "application/json"
    }

    # user = requests.get(f'{requrl}me', headers=session["auth_header"])
    # session["user"] = user["display_name"]

    return redirect("/visualize")


@app.route('/visualize')
def visualize():
    return render_template("visualize.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/analyze')
def analyze():

    currurl = 'https://api.spotify.com/v1/me/player/currently-playing'
    songreq = requests.get(currurl, headers=session["auth_header"])

    if songreq.status_code == 204:
        return jsonify({"content": "none"})
        
    songdata = songreq.json()

    if songdata["currently_playing_type"] == "ad":
        return jsonify({"content": "ad"})

    songname = songdata["item"]["name"]
    albumname = songdata["item"]["album"]["name"]
    artistname = songdata["item"]["album"]["artists"][0]["name"]
    songid = songdata["item"]["id"]
    songimg = songdata["item"]["album"]["images"][0]["url"]

    imgbuf = generate(songid, session["auth_header"])
    imgtag = "data:image/png;base64," + imgbuf

    response = {
       "songimg": songimg,
       "genimg": imgtag,
       "song": songname,
       "album": albumname,
       "artist": artistname
    }

    return jsonify(response)

@app.route('/refresh', methods=["GET", "POST"])
def refresh():

    refreshurl = 'https://accounts.spotify.com/api/token'

    refreshparams = {
        "grant_type": "refresh_token",
        "refresh_token": session['refresh_token']
    }

    refreshreq = requests.post(refreshurl, data=refreshparams, headers=session['accessheaders'])
    refreshdata = refreshreq.json()

    session.pop('access_token', None)
    session.pop('auth_header', None)

    session["access_token"] = refreshdata["access_token"]

    session["auth_header"] = {
        'Authorization': f'Bearer {session["access_token"]}',
        'CONTENT-TYPE': "application/json"
    }

    return "done"


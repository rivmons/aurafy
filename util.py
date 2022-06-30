import random
import string
import requests
from PIL import Image, ImageDraw, ImageFilter
from random import randint
from math import sqrt
from io import BytesIO
from base64 import b64encode, decode

from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("authorization_header") is None:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def randomstr(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def generate(id, authheader):
    
    # req url
    analysisurl = f'https://api.spotify.com/v1/audio-analysis/{id}'
    featuresurl = f'https://api.spotify.com/v1/audio-features/{id}'

    # get req
    analysisreq = requests.get(analysisurl, headers=authheader)
    featuresreq = requests.get(featuresurl, headers=authheader)

    # parse json data
    adata = analysisreq.json()
    fdata = featuresreq.json()

    data = {
        "features": {
            "acousticness": fdata["acousticness"],
            "danceability": fdata["danceability"],
            "energy": fdata["energy"],
            "instrumentalness": fdata["instrumentalness"],
            "loudness": fdata["loudness"],
            "speechiness": fdata["speechiness"],
            "tempo": fdata["tempo"],
            "time_signature": fdata["time_signature"],
            "valence": fdata["valence"]
        },

        "confidence": {
            "tempo_confidence": adata["track"]["tempo_confidence"],
            "time_signature_confidence": adata["track"]["time_signature"],
            "mode_confidence": adata["track"]["mode_confidence"],
        },
    }

    dataList = [fdata["energy"], fdata["danceability"], fdata["acousticness"], (fdata["time_signature"] - 3) / 4,
            fdata["valence"], fdata["tempo"] / 470, fdata["speechiness"], fdata["loudness"] / -60, fdata["liveness"], fdata["instrumentalness"]]

    # energy, danceability, acousticness, timeSig, valence, tempo,
    # speechiness, loudness, liveness, instrumentalness

    sad = [2.5, 1.25, 4, 1.15, 1.15, 2.35, 1.45, 2.5, 1.5, 3.75]
    happy = [3.8, 3.75, 2.65, 3.8, 4, 5, 2.6, 3.8, 3.75, 1.35]
    energetic = [4, 2.6, 1.3, 4.9, 3.8, 3.85, 3.85, 4, 4, 2.65]
    calm = [1.25, 4, 3.8, 2.25, 2.5, 1.4, 4, 1.35, 2.5, 4]

    # Acousticness: 4.29%
    # Danceability: .64%
    # Energy : 1.84%
    # Liveness: 3.43%
    # Loudness: .53%
    # Speechiness: 3.78%
    # Tempo: 1.28%
    # Valence: 6.10%
    # Total: 21.89%

    # weights (optional)
    weight = [1.084, 1.029, 1.196, 1.09, 1.5, 1.058, 1.173, 1.024, 1.157, 1.5]

    devList = [['sad', deviation(dataList, sad) - 0.2], ['happy', deviation(dataList, happy) - 0.7], ['energetic', deviation(dataList, energetic) - 0.75], ['calm', deviation(dataList, calm) - 0.5]]
    devList = sorted(devList, key=lambda x: x[1])

    img = generateimg(devList[0], devList[1])

    membuf = BytesIO()
    img.save(membuf, format="png")
    membuf.seek(0)

    return b64encode(membuf.getvalue()).decode()




def generateimg(primary, secondary):

    colors = {
        "calm": '#f8c8dc', # pink
        "happy": '#c1e1c1', # green
        "energetic": '#ffb079', # orange
        "sad": '#a7b4e8' # blue
    }
    

    totalweight = primary[1] + secondary[1]
    primarymood = primary[0]
    primaryweight = secondary[1] / totalweight
    secondarymood = secondary[0]
    secondaryweight = primary[1] / totalweight

    randcolors = []
    randcolors.append(colors[primarymood])
    randcolors.append(colors[secondarymood])
    pweight = colorweights(primarymood, primaryweight)
    sweight = colorweights(secondarymood, secondaryweight)
    randcolors.append(pweight)
    randcolors.append(sweight)

    w, h = 500, 700

    img = Image.new("RGB", (w, h))
    img1 = ImageDraw.Draw(img)
    img1.rounded_rectangle([(0, 0), (w, h*0.4)], fill=colors[primarymood])
    img1.rounded_rectangle([(0, h*0.4), (w, h*0.55)], fill=pweight)
    img1.rounded_rectangle([(0, h*0.6), (w, h*0.9)], fill=colors[secondarymood])
    img1.rounded_rectangle([(0, h*0.9), (w, h)], fill=sweight)

    # left polygon
    for i in range(2):
        y1 = randint(10, h - 10)
        img1.polygon([(0, y1), (randint(100, 300), randint(100, 450)), (0, (h - y1) * (randint(10, 100) / 100))], fill=randcolors[randint(0,3)], outline=colors[primarymood])

    # top polygon
    for i in range(2):
        x1 = randint(10, w - 10)
        img1.polygon([(x1, 0), (randint(100, 300), randint(100, 450)), (w, randint(0, h))], fill=randcolors[randint(0,3)], outline=colors[primarymood])

    # right polygon 
    for i in range(2):
        y1 = randint(10, h - 10)
        img1.polygon([(w, y1), (randint(100, 300), randint(100, 450)), (w, (h - y1) * (randint(10, 100) / 100))], fill=randcolors[randint(0,3)], outline=colors[primarymood])

    # random pieslice
    for i in range(2):
        z1 = randint(100, 200)
        x2 = randint(0, 500)
        y2 = randint(0, 500)
        dx = randint(100, 300)
        img1.pieslice([(x2, y2), (x2 + dx, y2 + dx)], z1, z1 + randint(0, 100), fill=randcolors[randint(0,3)])

    # random ellipse 
    for i in range(2):
        x3 = randint(0, 500)
        y3 = randint(0, 500)
        dx2 = randint(100, 300)
        img1.ellipse([(x3, y3), (x3 + dx2, y3 + dx2)], fill=randcolors[randint(0,3)])

    # bottom polygon
    for i in range(2):
        x1 = randint(10, w - 10)
        img1.polygon([(x1, h), (randint(100, 300), randint(100, 450)), (x1 + randint(0, 300), h)], fill=randcolors[randint(0,3)], outline=colors[primarymood])

    img = img.filter(ImageFilter.GaussianBlur(80))

    return img

    

def deviation(data, mean):
    weight = [1.084, 1.029, 1.196, 1.09, 1.5, 1.058, 1.173, 1.024, 1.157, 1.5]
    deviation = 0
    for i in range(10):
        deviation += (((data[i]*5) - mean[i]) * ((data[i]*5) - mean[i]) * weight[i])

    deviation = sqrt(deviation / (len(data) - 1))
    return deviation 

def colorweights(color, weight):

    colornames = {"calm": ["#F8E2EB", "#FA9DC3", "#FF82B5"], 
        "happy": ["#D3E0D3", "#A7E1A7", "#86E986"], 
        "energetic": ["#FCC49D", "#FF9E5B", "#FF9750"], 
        "sad": ["#C3CBEA", "#ADB5D7", "#90A1E7"]}
    

    if weight <= 0.48:
         return colornames[f'{color}'][0]
    if weight <= 0.525 and weight > 0.48:
        return colornames[f'{color}'][1]
    if weight > 0.525:
        return colornames[f'{color}'][2]


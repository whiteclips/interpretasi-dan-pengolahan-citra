from flask import Flask, render_template, Response, request, flash
from script.parseImg import *
from werkzeug.utils import secure_filename

import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    data = json.dumps({
        "short_name": "Image Processing App",
        "name": "Image Processing App",
        "icons": [
            {
            "src": "/static/image.png",
            "type": "image/png",
            "sizes": "256x256"
            }
        ],
        "start_url": "/index.html",
        "display": "standalone"
    })
    return Response(data, mimetype='application/x-web-app-manifest+json')

@app.route('/histogram')
def histogram():
    return render_template('histogram.html')

@app.route('/equalization')
def equalization():
    return render_template('equalization.html')

@app.route('/specification')
def specification():
    return render_template('specification.html')

@app.route('/text-reader')
def text_reader():
    return render_template('text-reader.html')

@app.route('/text-reader-process', methods=['POST'])
def text_reader_process():
    f = request.files['file']
    if (f):
        arr = getSegmentedImageArray(request.files['file'])
        dir, newArr = getDirectionFromArray(arr)
        if (dir.total() == 237):
            return '0'
        elif (dir.total() == 193):
            return '1'
        elif (dir.total() == 333):
            return '2'
        elif (dir.total() == 339):
            return '3'
        elif (dir.total() == 215):
            return '4'
        elif (dir.total() == 314):
            return '5'
        elif (dir.total() == 287):
            return '6'
        elif (dir.total() == 237):
            return '7'
        elif (dir.total() == 239):
            return '8'
        elif (dir.total() == 285):
            return '9'
        # print(arr)
        else:
            return dir.total
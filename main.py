from flask import Flask, render_template, Response, request, flash
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
        return f.filename
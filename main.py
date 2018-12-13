from flask import Flask, render_template, Response, request, flash, jsonify
from script.parseImg import *
from script.thin import *
import script.hand_written as hw
import script.operation as opt
import script.face_detector as fd
import script.face_recognition as fr
from werkzeug.utils import secure_filename
import uuid
import traceback
import json
import io
from PIL import Image

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
        "start_url": "/",
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
        models = trainModel()
        # arr = getSegmentedImageArray("./res/9.png")
        arr = getSegmentedImageArray(request.files['file'])
        dir, _ = getDirectionFromArray(arr)
        res = ""
        for d in dir:
            res += str(d.predict(models))
        return res

@app.route('/thinning')
def thinning():
    return render_template('thinning.html')

@app.route('/hand_recognition')
def hand_recognition():
    return render_template('hand_recognition.html')

@app.route('/hand_recognition', methods=['POST'])
def hand_recognition_process():
    try:
        f = request.files['file']
        pixel_treshold = request.form['pixel-treshold']
        noise_percentage = request.form['noise']
        print("Got pixel({}), noise({})".format(pixel_treshold,noise_percentage))
        if (f):
            arr = hw.getSegmentedImageArray(f, pixel_treshold)
            
            (skeletonized, tips, cross) = hw.skeletonizedImage(arr, float(noise_percentage))
            prediction = hw.predict(tips, cross)
            unique_filename = str(uuid.uuid4())
            path = 'static/dump/' + unique_filename + f.filename
            Image.fromarray(np.uint8(skeletonized)).save(path)

            return jsonify({'path' : path, 'prediction' : prediction})
    except:
        traceback.print_exc(file=sys.stdout)
        return jsonify({'path' : "", 'prediction' : "Something Wrong"})

@app.route('/thinning-process', methods=['POST'])
def thinning_process():
    f = request.files['file']
    if (f):
        noise_percentage = request.form['noise']
        # process file
        arr = getSegmentedImageArray(f)
        (skeletonized, tips, cross) = skeletonizedImage(arr, float(noise_percentage))
        # predict
        prediction = predict(tips, cross)
        unique_filename = str(uuid.uuid4())
        path = 'static/dump/' + unique_filename + f.filename
        Image.fromarray(np.uint8(skeletonized)).save(path)

        return jsonify({'path' : path, 'prediction' : prediction})

@app.route('/preprocessing')
def preprocessing():
    return render_template('preprocessing.html')

@app.route('/preprocess_image', methods=['POST'])
def preprocess_image():
    f = request.files['file']
    if (f):
        method = int(request.form['method'])
        m1 = request.form['matrix1'].split(",")
        m2 = request.form['matrix2'].split(",")

        image = Image.open(io.BytesIO(f.read()))
        path = opt.preprocess_image(image, method, m1, m2)
        return jsonify({'path' : path})

@app.route('/face_detection')
def face_detection():
    return render_template('face-detection.html')

@app.route('/face_detection_process', methods=['POST'])
def face_detection_process():
    f = request.files['file']
    if (f):

        image = Image.open(io.BytesIO(f.read()))
        path = fd.face_detect(image)
        return jsonify({'path' : path})

@app.route('/face_recognition')
def face_recognition():
    return render_template('face-recognition.html')

@app.route('/face_recognition_train')
def face_recognition_train():
    return render_template('face-recognition-train.html')

@app.route('/face_recognition_test')
def face_recognition_test():
    return render_template('face-recognition-test.html')

@app.route('/face_recognition_train_process', methods=['POST'])
def face_recognition_train_process():
    f = request.files['file']
    label = request.form['label']
    if (f):
        image = Image.open(io.BytesIO(f.read()))
        fr.train(image, label)
        return jsonify({'status' : label})

@app.route('/face_recognition_test_process', methods=['POST'])
def face_recognition_test_process():
    f = request.files['file']
    if (f):
        image = Image.open(io.BytesIO(f.read()))
        result = fr.predict(image)
        return jsonify({'label' : result})
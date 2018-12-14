import cv2
import pickle
import uuid
import os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from glob import glob


def crop_face(img_arr):
    face_cascade = cv2.CascadeClassifier('script/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('script/haarcascades/haarcascade_eye.xml')
#     gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    gray = img_arr
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        eyes_point = []
        for (ex, ey, ew, eh) in eyes:
            eye_point = [(x + ex, y + ey), (x + ex + ew, y + ey + eh)]
            eyes_point.append(eye_point)
    eyes_middle_point = []
    for eye_point in eyes_point:
        w = eye_point[1][0] - eye_point[0][0]
        h = eye_point[1][1] - eye_point[0][1]
        x = eye_point[0][0] + (w / 2)
        y = eye_point[0][1] + (h / 2)
        eyes_middle_point.append((x, y))

    # Applying formula of Golden Ratio from Pak Iping's paper
    x_left = eyes_middle_point[0][0]
    x_right = eyes_middle_point[1][0]
    y_left = eyes_middle_point[0][1]
    y_right = eyes_middle_point[1][1]
    distance_x = abs(x_right - x_left)
    x_center = int((x_left + x_right) / 2)
    y_center = int((y_left + y_right) / 2)
    x_a = int(((1.718 * x_left) - x_center) / 0.618)
    x_b = int(((1.518 * x_right) - x_center) / 0.618)
    y_d = int(y_center + (1.618 * distance_x))
    y_c = int(y_d - (1.618 * (y_d - y_center)))
    
    if (y_c > y_d):
        y_c, y_d = y_d, y_c
    if (x_b < x_a):
        x_a, x_b = x_b, x_a
#     print("X : {} {} {} {} ".format(x_a,x_b,y_d,y_c))
    
    image = img_arr[y_c:y_d, x_a:x_b]
    
    return scale_image(image)

def scale_image(image):
    current_height, current_width = image.shape
    wanted_width = 250
    wanted_height = 300
    print("Curr size: {} x {}".format(current_height, current_width))
    if current_height != wanted_height or current_width != wanted_width:
        image = cv2.resize(image, (wanted_width, wanted_height), interpolation=cv2.INTER_AREA)
    return image

def get_contour(x_arr):
    x_arr = gaussian_filter(x_arr, sigma=3) # Apply gaussian filter
    return x_arr

def crop_image(image):
    CROP_SIZE = 250
    BEGIN_CROP_X = 140
    BEGIN_CROP_Y = 80
    x = image.convert('L')
    x = np.asarray(x.getdata(), dtype=np.float64).reshape((x.size[1], x.size[0]))
    return Image.fromarray(x[BEGIN_CROP_X:BEGIN_CROP_X + CROP_SIZE, BEGIN_CROP_Y:BEGIN_CROP_Y + CROP_SIZE])


def fit_polynom(data):
    f = []
    size = data.shape[1]
    for i in range(data.shape[0]):
        f.append(np.poly1d(np.polyfit(np.arange(size), data[i, :], 10)))
    return f


def model_error(polynom, data):
    def error(y_true, y_pred):
        return np.average(np.abs(y_true - y_pred))
    print(data.shape)
    print(len(polynom))
    err = 0
    idx = np.arange(data.shape[1])
    for i in range(data.shape[0]):
        err += error(data[i, :], polynom[i](idx))
    return err / data.shape[0]


def save_model(model, label):
    f_name = os.getcwd() + '/model/' + label + '-' + uuid.uuid4().hex[:8] + '.ipg'
    with open(f_name, 'wb') as f:
        pickle.dump(model, f)


def load_model(f_name):
    model = None
    with open(f_name, 'rb') as f:
        model = pickle.load(f)
    return model


def train(image, label):
    print(os.getcwd())
    print(type(image))
    x=image.convert('L')
    x = np.asarray(x.getdata(),dtype='uint8').reshape((x.size[1],x.size[0]))
    # print(x.shape)
    # crop image
    x = crop_face(x)
    # preprocess image (contourizing)
    contour_arr = get_contour(x)
    # fit model
    print(contour_arr.shape)
    polynoms = fit_polynom(contour_arr)
    # save model
    model = {
        'label': label,
        'polynom': polynoms
    }
    save_model(model, label)
    print("trained")


def predict(image):
    x=image.convert('L')
    x = np.asarray(x.getdata(),dtype='uint8').reshape((x.size[1],x.size[0]))
    # crop image
    x = crop_face(x)
    # preprocess image (contourizing)
    contour_arr = get_contour(x)
    # evaluate
    f_names = glob(os.getcwd() + '/model/*.ipg')
    error_models = []
    for f_name in f_names:
        model = load_model(f_name)
        error_models.append({
            'label': model['label'],
            'error': model_error(model['polynom'], contour_arr)
        })

    # Find minimum
    min_err = error_models[0]['error']
    label = error_models[0]['label']
    for e_mdl in error_models:
        if (e_mdl['error'] < min_err):
            label = e_mdl['label']
            min_err = e_mdl['error']
    # print(error_models)
    # print(label)
    # label = ""
    return (error_models, label)

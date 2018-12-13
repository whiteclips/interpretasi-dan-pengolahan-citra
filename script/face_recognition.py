import pickle
import uuid
import os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from glob import glob



def get_contour(image):
    x = image.convert('L') # makes it greyscale
    x_arr = np.asarray(x.getdata(),dtype=np.float64).reshape((x.size[1],x.size[0]))
    x_arr = gaussian_filter(x_arr, sigma=3) # Apply gaussian filter
    return x_arr

def crop_image(image):
    CROP_SIZE=250
    BEGIN_CROP_X = 140
    BEGIN_CROP_Y = 80
    x=image.convert('L')
    x=np.asarray(x.getdata(),dtype=np.float64).reshape((x.size[1],x.size[0]))
    return Image.fromarray(x[BEGIN_CROP_X:BEGIN_CROP_X+CROP_SIZE,BEGIN_CROP_Y:BEGIN_CROP_Y+CROP_SIZE])

def fit_polynom(data):
    f = []
    size = data.shape[0]
    for i in range(size):
        f.append(np.poly1d(np.polyfit(np.arange(size), data[i,:], 10)))
    return f

def model_error(polynom, data):
    def error(y_true,y_pred):
        return np.average(np.abs(y_true-y_pred)) 
    err = 0
    idx = np.arange(data.shape[0])
    for i in range(data.shape[0]):
        err += error(data[i,:], polynom[i](idx))
    return err/data.shape[0]

def save_model(model,label):
    f_name = os.getcwd()+'/model/'+label+'-'+uuid.uuid4().hex[:8] + '.ipg'
    with open(f_name,'wb') as f:
        pickle.dump(model, f)

def load_model(f_name):
    model = None
    with open(f_name,'rb') as f:
        model = pickle.load(f)
    return model

def train(image, label):
    # crop image
    x = crop_image(image)
    # preprocess image (contourizing)
    contour_arr = get_contour(x)
    # fit model
    print(contour_arr.shape)
    polynoms = fit_polynom(contour_arr)
    # save model
    model = {
        'label':label,
        'polynom':polynoms
    }
    save_model(model,label)
    print("trained")

def predict(image):
    # crop image
    x = crop_image(image)
    # preprocess image (contourizing)
    contour_arr = get_contour(x)
    # evaluate
    f_names = glob(os.getcwd()+'/model/*.ipg')
    error_models = []
    for f_name in f_names:
        model = load_model(f_name)
        error_models.append({
            'label':model['label'],
            'error':model_error(model['polynom'],contour_arr)
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
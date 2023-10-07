import os
import settings
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

SIZE = 256

def get_max_min_wh():

    db_path = settings.SAVE_DB

    w_min = None
    w_max = None
    h_min = None
    h_max = None

    for path in os.listdir(db_path):

        im = Image.open(os.path.join(db_path, path))
        w, h = im.size

        if not w_min: w_min = w
        if not w_max: w_max = w
        if not h_min: h_min = h
        if not h_max: h_max = h
        
        if w > w_max: w_max = w
        if w < w_min: w_min = w
        if h > h_max: h_max = h
        if h < h_min: h_min = h
        
    
    return w_min, w_max, h_min, h_max

W_MIN, W_MAX, H_MIN, H_MAX = get_max_min_wh()

def cut_from_middle():

    db_path = settings.SAVE_DB

    for path in os.listdir(db_path):
        im_path = os.path.join(db_path, path)
        im = Image.open(im_path)

        w, h = im.size
        center = w//2, h//2
        im = im.crop(box=(center[0]-SIZE//2, center[1]-SIZE//2, center[0]+SIZE//2, center[1]+SIZE//2))

        im.save(im_path)
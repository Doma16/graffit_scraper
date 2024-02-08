import os
import settings
import numpy as np
from tqdm import tqdm
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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

def visualize(imgs, labels):
    #imgs = imgs.reshape(imgs.shape[0], 256, 256, 3)
    n_ = 2
    pca = PCA(n_components=n_)
    x_pca = pca.fit_transform(imgs)
    plt.scatter(x_pca[:, 0], x_pca[:, 1], c=labels)
    plt.title('PCA analysis')
    plt.colorbar()
    plt.show()
    

def cluster():

    db_path = settings.SAVE_DB

    db_len = len(os.listdir(db_path))
    batch = 256
    clusters = 10
    kmeans = None

    for id in tqdm(range(0, db_len, batch)):
        imgs = []
        for path in os.listdir(db_path)[id:id+batch]:
            im_path = os.path.join(db_path, path)

            im = Image.open(im_path)
            im = np.array(im)
            im = im.reshape(-1)
            imgs.append(im)

        imgs = np.stack(imgs)
    
        if not kmeans:
            kmeans = KMeans(n_clusters=clusters, random_state=0, n_init='auto').fit(imgs)
        else:
            kmeans.fit(imgs)
        # To visualize results with PCA
        # visualize(imgs, kmeans.labels_)

    db_cluster_path = settings.SAVE_CLUSTER

    for id in tqdm(range(0, db_len, batch)):
        imgs = []
        for path in os.listdir(db_path)[id:id+batch]:
            im_path = os.path.join(db_path, path)

            im = Image.open(im_path)
            im = np.array(im)
            im = im.reshape(-1)
            imgs.append(im)

        imgs = np.stack(imgs)

        labels = kmeans.predict(imgs)

        for label in range(clusters):
            
            for img in imgs[labels == label]:
                im = img.reshape(256,256,3)
                im = Image.fromarray(im)
                s_path = os.path.join(db_cluster_path, f'{label}', f'l{label}_{id}'+'.png')
                im.save(s_path)

    print('...')
    print('Still have to somehow guess which cluster is bad, for example white-black ones are usually bad')
    breakpoint()
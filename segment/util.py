import os
import numpy as np
import matplotlib.pyplot as plt

def iter_imgs(path):
    images = os.listdir(path)
    return images

def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)

def show_mask(masks, ax, random_color=False):
    for mask in masks:
        if random_color:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
        else:
            color = np.array([30/255, 144/255, 255/255, 0.6])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        ax.imshow(mask_image)

def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    

def mask_test():
    from .model import SAM
    import settings
    import cv2

    images = iter_imgs(settings.SAVE_DB)[:10]
    sam = SAM()

    pcent = 0.5

    for id, image in enumerate(images):
        img = cv2.imread(os.path.join(settings.SAVE_DB, image))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        h, w, _ = img.shape
        coords = w/2 * (1-pcent), h/2 * (1+pcent), w/2 * (1+pcent), h/2 * (1-pcent) #xyxy
        box = np.array([*coords])

        sam.set(img)
        masks = sam.segment(img, box)

        plt.figure(figsize=(20,20))
        plt.imshow(np.zeros(img.shape))
        #show_anns(masks)
        show_mask(masks, plt.gca(), random_color=True)
        show_box(box, plt.gca())
        plt.savefig(os.path.join(settings.SAVE_MASKS, f'{id}_{image[:-4]}.png'))

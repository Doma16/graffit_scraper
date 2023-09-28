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

def mask_test():
    from .model import SAM
    import settings
    import cv2

    images = iter_imgs(settings.SAVE_DB)[:10]
    sam = SAM()

    for id, image in enumerate(images):
        img = cv2.imread(os.path.join(settings.SAVE_DB, image))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        masks = sam.segment(img)

        plt.figure(figsize=(20,20))
        plt.imshow(np.zeros(img.shape))
        show_anns(masks)
        plt.savefig(os.path.join(settings.SAVE_MASKS, f'{id}_{image[:-4]}.png'))

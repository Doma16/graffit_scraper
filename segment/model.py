from segment_anything import sam_model_registry, SamPredictor, SamAutomaticMaskGenerator
import numpy as np
import settings

class SAM:

    def __init__(self, model_type=settings.MODEL_TYPE, model_path=settings.SAM_PATH, device='cpu'):
        
        self.model_type = model_type
        self.model_path = model_path
        self.device = device

        self.sam = sam_model_registry[model_type](checkpoint=model_path)
        self.sam.to(device=device)

        self.mask_generator = SamAutomaticMaskGenerator(self.sam)

    def set(self, image):
        self.predictor = SamPredictor(self.sam)
        self.predictor.set_image(image)

    def segment(self, img, box=None):
        
        if type(box) == type(None):
            masks = self.mask_generator.generate(img)
        else:
            x, y = (box[0] + box[2])/2, (box[1] + box[3])/2
            masks, _, _ = self.predictor.predict(
                point_coords=np.array([[x,y]]),
                point_labels=np.array([0]),
                box=box[None, :],
                multimask_output=True)
            
        return masks



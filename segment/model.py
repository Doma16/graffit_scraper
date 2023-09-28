from segment_anything import sam_model_registry, SamPredictor, SamAutomaticMaskGenerator
import settings

class SAM:

    def __init__(self, model_type=settings.MODEL_TYPE, model_path=settings.SAM_PATH, device='cpu'):
        
        self.model_type = model_type
        self.model_path = model_path
        self.device = device

        self.sam = sam_model_registry[model_type](checkpoint=model_path)
        self.sam.to(device=device)

        self.mask_generator = SamAutomaticMaskGenerator(self.sam)

    def segment(self, img):
        
        masks = self.mask_generator.generate(img)

        return masks



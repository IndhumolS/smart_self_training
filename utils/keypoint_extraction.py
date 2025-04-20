import cv2
import numpy as np
import torch
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import os
from models.keypoint_model import KeypointModel

# Load Detectron2 model
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
predictor = DefaultPredictor(cfg)


def extract_keypoints(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"❌ Error loading image: {image_path}")
        return None

    outputs = predictor(image)
    instances = outputs["instances"]

    if instances.has("pred_keypoints"):
        keypoints = instances.pred_keypoints.cpu().numpy()
        return keypoints.tolist()
    else:
        print(f"⚠️ No keypoints detected in {os.path.basename(image_path)}, skipping.")
        return None

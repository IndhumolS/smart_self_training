# utils/predict_util.py

import cv2
import numpy as np
import torch
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import joblib
from models.keypoint_model import KeypointModel

# Load Detectron2 config
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
predictor = DefaultPredictor(cfg)

# Load trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = KeypointModel().to(device)
model.load_state_dict(torch.load("models/best_model.pth", map_location=device))
model.eval()

label_mapping = {
    0: "badminton_drive_shot",
    1: "badminton_drop_shot",
    2: "badminton_smash_shot",
    3: "cricket_cover_drive",
    4: "cricket_cut_shot",
    5: "cricket_sweep_shot",
    6: "tennis_serve",
    7: "tennis_smash",
    8: "tennis_volley"
}


# Load label encoder
encoder = joblib.load("models/label_encoder.pkl")

def extract_keypoints(image_np):
    outputs = predictor(image_np)
    instances = outputs["instances"]
    if instances.has("pred_keypoints"):
        keypoints = instances.pred_keypoints.cpu().numpy()
        return keypoints.tolist()
    return None

def flatten_keypoints(keypoints):
    flattened = []
    for person in keypoints:
        for point in person:
            flattened.append(point[0])
            flattened.append(point[1])
        break
    while len(flattened) < 34:
        flattened.append(0.0)
    return flattened[:34]

def scale_keypoints(kp):
    IMAGE_WIDTH = 220
    IMAGE_HEIGHT = 165
    scaled = []
    for i in range(0, len(kp), 2):
        x = kp[i] / IMAGE_WIDTH
        y = kp[i+1] / IMAGE_HEIGHT
        scaled.extend([x, y])
    return scaled

def normalize_keypoints(kp_scaled):
    return [(val - 0.5) * 2 for val in kp_scaled]

def predict_shot_from_image_file(image_path):
    image_np = cv2.imread(image_path)
    if image_np is None:
        raise ValueError("Could not load image from path.")

    keypoints = extract_keypoints(image_np)
    if not keypoints:
        raise ValueError("No keypoints detected.")

    flattened = flatten_keypoints(keypoints)
    scaled = scale_keypoints(flattened)
    normalized = normalize_keypoints(scaled)

    input_tensor = torch.tensor([normalized], dtype=torch.float32).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs.data, 1)
        predicted_label = predicted.item()
        shot_name = label_mapping[predicted_label]
        return shot_name

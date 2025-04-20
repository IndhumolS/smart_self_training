# routes/predict.py
from fastapi import APIRouter, UploadFile, File
from utils.predict_util import predict_shot_from_image_file

router = APIRouter()

@router.post("/predict_shot/")
async def predict_shot(image_file: UploadFile = File(...)):
    try:
        shot_name = await predict_shot_from_image_file(image_file)
        return {"shot_name": shot_name}
    except Exception as e:
        return {"error": str(e)}

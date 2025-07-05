# routes/predict.py

from fastapi import APIRouter, UploadFile, File, Depends
from utils.predict_util import predict_shot_from_image_file
from database.mongodb import get_database
from datetime import datetime

router = APIRouter()

@router.post("/predict_shot/")
async def predict_shot(image_file: UploadFile = File(...), db=Depends(get_database)):
    try:
        # 1. Perform prediction
        shot_name = await predict_shot_from_image_file(image_file)

        # 2. Save prediction log to database
        db["prediction_logs"].insert_one({
            
            "shot_name": shot_name,
            "timestamp": datetime.now(),
            "filename": image_file.filename
        })

        return {"shot_name": shot_name}

    except Exception as e:
        return {"error": str(e)}

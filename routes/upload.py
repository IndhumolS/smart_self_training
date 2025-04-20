from fastapi import APIRouter, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from database.mongodb import video_collection
import shutil
import os
from utils.predict_util import predict_shot_from_image_file
from database.mongodb import  get_user_by_username,get_video_by_shot_type
router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-image", response_class=HTMLResponse)
async def upload_image(
    request: Request,
    image: UploadFile = File(...),
    keypoints: str = Form(...),  # Add keypoints here if needed
    user_name: str = Form(...)
):

    try:
        # Predict the shot type
        predicted_shot_type = await predict_shot_from_image_file(image)

        # Fetch video URL from DB
        video_doc = get_video_by_shot_type(predicted_shot_type)
        video_url = video_doc.get("video_url") if video_doc else None


        # Get user details
        user = get_user_by_username(user_name)

        return templates.TemplateResponse("player_dashboard.html", {
            "request": request,
            "user": user,
            "predicted_shot_type": predicted_shot_type,
            "video_url": video_url
        })

    except Exception as e:
        # Re-render dashboard with error message
        user = get_user_by_username(user_name)
        return templates.TemplateResponse("player_dashboard.html", {
            "request": request,
            "user": user,
            "error_message": f"Error during prediction: {str(e)}"
        })
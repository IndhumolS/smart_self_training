from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database.mongodb import video_collection, user_collection
import os
import shutil
from utils.predict_util import predict_shot_from_image_file

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/upload-image", response_class=HTMLResponse)
async def upload_image(request: Request, image: UploadFile = File(...)):
    user_email = request.cookies.get("user_email")
    user = user_collection.find_one({"email": user_email})
    
    if not user:
        return templates.TemplateResponse("index.html", {"request": request, "error": "User not found."})

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, image.filename)

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    try:
        # Pass empty list for keypoints if you're not using them during prediction
        detected_shot = predict_shot_from_image_file(temp_path)


    except Exception as e:
        os.remove(temp_path)
        return templates.TemplateResponse("player_dashboard.html", {
            "request": request,
            "prediction": f"Error during prediction: {str(e)}",
            "video_url": None,
            "user": user
        })

    os.remove(temp_path)

    video_doc = video_collection.find_one({"shot_type": detected_shot})
    video_url = video_doc["video_url"] if video_doc else None

    return templates.TemplateResponse("player_dashboard.html", {
        "request": request,
        "prediction": detected_shot,
        "video_url": video_url,
        "user": user
    })

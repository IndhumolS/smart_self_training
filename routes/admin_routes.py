from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from database.mongodb import video_collection
import shutil, os

router = APIRouter()

@router.post("/upload-video")
async def upload_video(game: str = Form(...), shot: str = Form(...), video: UploadFile = File(...)):
    video_folder = "static/videos"
    os.makedirs(video_folder, exist_ok=True)

    video_path = os.path.join(video_folder, f"{shot}.mp4")

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    video_url = f"/static/videos/{shot}.mp4"

    # Store in MongoDB
    video_doc = {
        "game": game,
        "shot_type": shot,
        "video_url": video_url
    }
    video_collection.insert_one(video_doc)

    return HTMLResponse(content="Video uploaded successfully!")

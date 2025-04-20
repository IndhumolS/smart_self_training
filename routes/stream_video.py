from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from bson import ObjectId
from io import BytesIO

from database.mongodb import fs  # Expose fs from mongodb.py

router = APIRouter()

@router.get("/video/{video_id}")
def serve_video(video_id: str):
    try:
        grid_out = fs.get(ObjectId(video_id))
        return StreamingResponse(BytesIO(grid_out.read()), media_type="video/mp4")
    except Exception as e:
        return {"error": f"Video not found or invalid ID: {str(e)}"}

from fastapi import APIRouter
from database.mongodb import get_video_collection

router = APIRouter()
video_collection = get_video_collection()

@router.post("/insert-all-videos")
def insert_all_videos():
    videos = [
        {"shot_type": "badminton_drive_shot", "video_url": "/static/videos/badminton_drive_shot.mp4"},
        {"shot_type": "badminton_drop_shot", "video_url": "/static/videos/badminton_drop_shot.mp4"},
        {"shot_type": "badminton_smash_shot", "video_url": "/static/videos/badminton_smash_shot.mp4"},
        {"shot_type": "cricket_cover_drive", "video_url": "/static/videos/cricket_cover_drive.mp4"},
        {"shot_type": "cricket_cut_shot", "video_url": "/static/videos/cricket_cut_shot.mp4"},
        {"shot_type": "cricket_sweep_shot", "video_url": "/static/videos/cricket_sweep_shot.mp4"},
        {"shot_type": "tennis_serve", "video_url": "/static/videos/tennis_serve.mp4"},
        {"shot_type": "tennis_smash", "video_url": "/static/videos/tennis_smash.mp4"},
        {"shot_type": "tennis_volley", "video_url": "/static/videos/tennis_volley.mp4"},
    ]

    inserted_videos = []
    skipped_videos = []

    for video in videos:
        existing = video_collection.find_one({"shot_type": video["shot_type"]})
        if existing:
            skipped_videos.append(video["shot_type"])
        else:
            result = video_collection.insert_one(video)
            inserted_videos.append(str(result.inserted_id))

    return {
        "message": "✅ Video insertion complete.",
        "inserted": inserted_videos,
        "skipped (already existed)": skipped_videos
    }

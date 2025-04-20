# upload_video.py
import os
from pymongo import MongoClient
import gridfs

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["smart_self_training"]
fs = gridfs.GridFS(db)
videos_collection = db["videos"]

# Folder containing sample videos
video_folder ="static/videos"


# Map: shot type → filename (exact match with label_mapping)
video_map = {
    "badminton_drive_shot": "badminton_drive_shot.mp4",
    "badminton_drop_shot": "badminton_drop_shot.mp4",
    "badminton_smash_shot": "badminton_smash_shot.mp4",
    "cricket_cover_drive": "cricket_cover_drive.mp4",
    "cricket_cut_shot": "cricket_cut_shot.mp4",
    "cricket_sweep_shot": "cricket_sweep_shot.mp4",
    "tennis_serve": "tennis_serve.mp4",
    "tennis_smash": "tennis_smash.mp4",
    "tennis_volley": "tennis_volley.mp4"
}

for shot_type, filename in video_map.items():
    video_path = os.path.join(video_folder, filename)
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        continue

    with open(video_path, "rb") as f:
        video_id = fs.put(f, filename=filename)

    videos_collection.insert_one({
        "shot_type": shot_type,
        "video_id": video_id,
        "video_url": f"/video/{video_id}"
    })

    print(f"Uploaded: {filename} as {shot_type}")

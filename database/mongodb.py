# Fastapi_backend/database/mongodb.py

from pymongo import MongoClient
import gridfs
import os

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["smart_self_training"]

# Create collections if not exist
if "users" not in db.list_collection_names():
    db.create_collection("users")
    print("✅ 'users' collection created.")
else:
    print("ℹ️ 'users' collection already exists.")

if "videos" not in db.list_collection_names():
    db.create_collection("videos")
    print("✅ 'videos' collection created.")
else:
    print("ℹ️ 'videos' collection already exists.")

# Ensure unique index on email
db.users.create_index("email", unique=True)

# Create index on shot_type in the videos collection
db.videos.create_index("shot_type", unique=False)

# Access collections
user_collection = db["users"]
video_collection = db["videos"]

# GridFS instance
fs = gridfs.GridFS(db)

# ----------------- FUNCTIONS -------------------

def get_user_collection():
    return user_collection

def get_video_collection():
    return video_collection

def upload_video_to_gridfs(video_path: str, video_name: str, label: str):
    if not os.path.exists(video_path):
        print(f"❌ Video file not found at path: {video_path}")
        return None

    # Avoid re-uploading if file already exists
    existing = db.fs.files.find_one({"filename": video_name})
    if existing:
        print(f"⚠️ '{video_name}' already exists in GridFS. Skipping.")
        return None

    # Upload to GridFS
    with open(video_path, "rb") as f:
        video_id = fs.put(f, filename=video_name, metadata={"label": label})
        print(f"✅ Video '{video_name}' uploaded successfully with ID: {video_id}")

        # Store reference in videos collection
        video_data = {
            "shot_type": label,
            "filename": video_name,
            "video_id": video_id,
            "video_url": f"/video/{video_id}"  # ✅ Changed 'url' → 'video_url'
        }
        video_collection.insert_one(video_data)
        return video_id

def get_video_url(predicted_shot_type: str):
    video = video_collection.find_one({"shot_type": predicted_shot_type})
    if video:
        return video.get("video_url", None)  # ✅ Now matches what’s stored
    return None

def get_user_by_email(email: str):
    return user_collection.find_one({"email": email})

def update_user_profile(email: str, name: str, password: str):
    result = user_collection.update_one(
        {"email": email},
        {"$set": {"name": name, "password": password}}
    )
    return result.modified_count > 0

def get_video_by_shot_type(shot_type):
    video_doc = video_collection.find_one({"shot_type": shot_type})
    if video_doc and "video_id" in video_doc:
        return video_doc
    return None  # ✅ Return None instead of string for consistency

def get_user_by_username(username: str):
    return user_collection.find_one({"username": username})

# insert_admin.py

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["smart_self_training"]
user_collection = db["users"]

# Admin data to be inserted
admin_data = {
    "fullname": "Admin",
    "email": "admin@smarttrain.com",
    "phone": "1234567890",
    "username": "admin",
    "password": "admin123",  # You can use password hashing here if needed
    "role": "admin",
    "profile_picture": None
}

# Insert only if not already exists
existing_admin = user_collection.find_one({"email": admin_data["email"], "role": "admin"})
if existing_admin:
    print("✅ Admin already exists.")
else:
    user_collection.insert_one(admin_data)
    print("✅ Admin added successfully.")

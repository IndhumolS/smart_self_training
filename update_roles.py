from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["smart_self_training"]
users_collection = db["users"]

# Update all users who don't have a 'role' field
users_collection.update_many(
    {"role": {"$exists": False}},
    {"$set": {"role": "user"}}
)

print("Role field added to existing users.")

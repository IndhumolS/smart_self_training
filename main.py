from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from pymongo import MongoClient
from routes import auth, predict, profile  # Import the auth router
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from utils.predict_util import predict_shot_from_image_file
from starlette.middleware.sessions import SessionMiddleware
from models import user
from routes import player_routes, admin_routes
from routes.stream_video import router as stream_video_router
import os
import json
from utils.jwt import get_email_from_token

# Initialize the FastAPI app
app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["smart_self_training"]
user_collection = db["users"]

# Ensure upload directory exists
Path("static/uploads").mkdir(parents=True, exist_ok=True)

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Session Middleware for handling sessions
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Setup Jinja Templates
templates = Jinja2Templates(directory="templates")

# Include route files
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(profile.router)
app.include_router(player_routes.router)
app.include_router(admin_routes.router)
app.include_router(stream_video_router)

# Define User Model
class User(BaseModel):
    username: str
    email: str
    password: str

# Simulate fetching the current user from the session or database
def get_current_user(request: Request) -> User:
    email = request.cookies.get("user_email")
    if not email:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    user_data = user_collection.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user_data)

# Routes

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about():
    with open("templates/about.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.get("/contact", response_class=HTMLResponse)
async def contact():
    with open("templates/contact.html", "r") as file:
        return HTMLResponse(content=file.read())

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_user(
    request: Request,
    fullname: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    profile_picture: UploadFile = File(None),
    terms: str = Form(...)
):
    role = "player"  # Set default role
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if user_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    profile_path = None
    if profile_picture:
        file_location = Path(f"static/uploads/{profile_picture.filename}")
        with open(file_location, "wb") as f:
            f.write(await profile_picture.read())
        profile_path = str(file_location)

    user_collection.insert_one({
        "fullname": fullname,
        "email": email,
        "phone": phone,
        "username": username,
        "password": password,
        "role": role,
        "profile_picture": profile_path
    })

    return RedirectResponse(url="/register?success=true", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(
    request: Request,
    role: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user = user_collection.find_one({"email": email, "password": password, "role": role})

    if user:
        response = None
        if role == "admin":
            response = templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": user})
        elif role == "player":
            response = templates.TemplateResponse("player_dashboard.html", {"request": request, "user": user})
    
        if response:
            response.set_cookie(key="user_email", value=user["email"])
            return response

    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials or role"})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user_by_email(email: str):
    user_data = await user_collection.find_one({"email": email})
    return user_data

@app.get("/edit-profile")
async def edit_profile(request: Request, token: str = Depends(oauth2_scheme)):
    user_email = await get_email_from_token(token)
    user_data = await get_user_by_email(user_email)
    return templates.TemplateResponse("edit_profile.html", {"request": request, "user": user_data})

@app.post("/save-profile")
async def save_profile(username: str, email: str, current_user: User = Depends(get_current_user)):
    user_collection.update_one(
        {"email": current_user.email},
        {"$set": {"username": username, "email": email}}
    )
    return RedirectResponse(url="/edit-profile", status_code=303)

# ❌ Removed the /upload-image route from here — it's handled in player_routes.py now

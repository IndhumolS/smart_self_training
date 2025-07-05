from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database.mongodb import get_user_collection
from database.mongodb import get_user_by_email, update_user_profile
from starlette.status import HTTP_303_SEE_OTHER
from pymongo import MongoClient
import os
from starlette.status import HTTP_302_FOUND

client = MongoClient("mongodb://localhost:27017")
db = client["smart_self_training"]

if "users" not in db.list_collection_names():
    db.create_collection("users")
    print("✅ 'users' collection created.")
else:
    print("ℹ️ 'users' collection already exists.")

db.users.create_index("email", unique=True)
user_collection = get_user_collection()

templates = Jinja2Templates(directory="templates")
router = APIRouter()

# ============================ REGISTER =============================
@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
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
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = user_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    profile_path = None
    if profile_picture:
        file_location = f"static/uploads/{profile_picture.filename}"
        with open(file_location, "wb") as f:
            f.write(await profile_picture.read())
        profile_path = file_location

    user_collection.insert_one({
        "fullname": fullname,
        "email": email,
        "phone": phone,
        "username": username,
        "password": password,
        "profile_picture": profile_path,
        "role": "user"
    })

    return templates.TemplateResponse("login.html", {"request": request, "success": "Registration successful!"})


# ============================ LOGIN =============================
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_user(
    request: Request,
    role: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        user = user_collection.find_one({"email": email, "password": password})
        if user:
            user_role = user.get("role", "player")
            if user_role == role:
                request.session["user"] = email  # ✅ Set session
                if role == "admin":
                    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": user})
                elif role == "player":
                    return templates.TemplateResponse("player_dashboard.html", {"request": request, "user": user})
            else:
                return templates.TemplateResponse("login.html", {
                    "request": request,
                    "error": "Incorrect role selected for this account."
                })

        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid email or password."
        })

    except Exception as e:
        print("❌ Login Error:", e)
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Internal Server Error. Please try again later."
        })


# ============================ EDIT PROFILE =============================

@router.get("/profile")
async def view_profile(request: Request):
    user_email = request.session.get("user")
    if not user_email:
        return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)

    user = await get_user_by_email(user_email)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@router.get("/profile/edit")
async def edit_profile_form(request: Request):
    user_email = request.session.get("user")
    if not user_email:
        return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)

    user = get_user_by_email(user_email)
    return templates.TemplateResponse("edit_profile.html", {"request": request, "user": user})

@router.post("/profile/edit")
async def edit_profile(request: Request,
                       name: str = Form(...),
                       password: str = Form(...)):
    user_email = request.session.get("user")
    if not user_email:
        return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)

    await update_user_profile(user_email, name=name, password=password)
    return RedirectResponse("/profile", status_code=HTTP_303_SEE_OTHER)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/edit-profile", response_class=HTMLResponse)
async def edit_profile(request: Request):
    return templates.TemplateResponse("edit_profile.html", {"request": request})



@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)
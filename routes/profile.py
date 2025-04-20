from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database.mongodb import get_user_collection, update_user_profile,db
from starlette.status import HTTP_302_FOUND
from bson.json_util import dumps
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="templates")

user_collection = get_user_collection()

@router.get("/profile", response_class=HTMLResponse)
async def view_profile(request: Request):
    user_email = request.session.get("user")  # Make sure session contains 'user' (email)
    if not user_email:
        return RedirectResponse("/login", status_code=302)

    user_data = user_collection.find_one({"email": user_email})

    return templates.TemplateResponse("profile.html", {"request": request, "user": user_data})


@router.get("/edit-profile", response_class=HTMLResponse)
def edit_profile(request: Request):
    user_email = request.session.get("user")
    user_data = user_collection.find_one({"email": user_email})
    return templates.TemplateResponse("edit_profile.html", {"request": request, "user": user_data})

@router.post("/save-profile")
async def save_profile(
    request: Request,
    username: str = Form(...),
    email: str = Form(...)
):
    print("✔️ Username:", username)
    print("✔️ Email:", email)
    # You can update the database here
    return {"message": "Profile updated"}
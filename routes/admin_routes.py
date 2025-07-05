from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from database.mongodb import user_collection, db, get_database

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Admin Dashboard Route
@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    db = get_database()

    # Fetch users with role 'player' and prediction logs
    users = list(db["users"].find({"role": "player"}, {"_id": 0}))
    logs = list(db["prediction_logs"].find({}, {"_id": 0}))
    
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "users": users,
        "prediction_logs": logs
    })

# Delete User Route
@router.post("/admin/delete-user")
async def delete_user(username: str = Form(...)):
    # Check if user exists before deleting
    user = user_collection.find_one({"username": username})
    if not user:
        return {"error": "User not found."}

    user_collection.delete_one({"username": username})  # Delete the user
    return RedirectResponse(url="/admin/dashboard", status_code=HTTP_302_FOUND)

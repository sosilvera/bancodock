from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse

router = APIRouter(prefix="/elegion")

@router.get("/")
async def read_root():
    # Redirect a /login
    return RedirectResponse(url="/elegion/login")

@router.get("/login")
async def read_login():
    return FileResponse("static/login.html")

@router.get("/account")
async def read_account():
    return FileResponse("static/home.html")
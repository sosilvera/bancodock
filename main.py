import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.api_routes import router as api_router
from routes.static_routes import router as static_router


from commons.querys import Querys
import data as t

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar CORS para desarrollo
origins = ["*"]  # Esto permitirá cualquier origen (solo para desarrollo)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(static_router)
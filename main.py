from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from config import DOTENV_PATH
from app.routes import router
from app.routes.account_statements_routes import router as account_router

load_dotenv(DOTENV_PATH)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.include_router(account_router)


@app.get("/", tags=["root"])
def hello():
    return "Hello world"

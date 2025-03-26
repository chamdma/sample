from fastapi import FastAPI
from routes import router   
from models import User
import utils

app = FastAPI()


app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

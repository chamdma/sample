from fastapi import FastAPI
from routes import router as user_router

app=FastAPI()

app.include_router(user_router, prefix="/users")


@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


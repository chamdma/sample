from fastapi import FastAPI, Request, APIRouter, Depends

from models import User
from auth import create_access_token, verify_access_token

router = APIRouter()




@router.post("/")
async def create_user(request: Request):
    try:
        data = await request.json()  
    except Exception:
        return {
            "status_code": 400,
            "description": "Invalid JSON format",
            "status": False,
            "data": [],
        }

    required_fields = ["user_id", "username", "email", "password", "age", "address"]
    if not all(field in data for field in required_fields):
        return {
            "status_code": 400,
            "description": "Missing required fields",
            "status": False,
            "data": [],
        }

    try:
        new_user = User(**data)
        new_user.save()
    except Exception as e:
        return {
            "status_code": 500,
            "description": f"Error creating user: {str(e)}",
            "status": False,
            "data": [],
        }

    access_token = create_access_token({"user_id": new_user.user_id})  

    return {
        "status_code": 200,
        "description": "User created successfully",
        "status": True,
        "access_token": access_token,
        "data": new_user.to_mongo().to_dict(),
    }





@router.put("/update")
async def update_user(request: Request, token_data: dict = Depends(verify_access_token)):
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        return {"status_code": 400, "description": "user_id is required", "status": False, "data": []}

    existing_user = User.objects(user_id=user_id).first()
    existing_user.update(**{"set__{key}": value for key, value in data.items() if key != "user_id"})

    return { "User updated successfully"}






@router.delete("/users")
async def delete_user(request: Request, token_data: dict = Depends(verify_access_token)):
    data = await request.json()
    user_id = data.get("user_id")

    user = User.objects(user_id=user_id).first()
    user.delete()
    return {"User deleted successfully"}





@router.get("/users")
async def list_users(token_data: dict = Depends(verify_access_token)):
    users = User.objects().exclude("id")
    return {
        "status_code": 200,
        "description": "Users retrieved successfully",
        "status": True,
        "data": [user.to_mongo().to_dict() for user in users],
    }
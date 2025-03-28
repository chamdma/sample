from fastapi import FastAPI, Request, APIRouter, Depends,Body,Header
from models import User
from utils import create_access_token

router = APIRouter()


@router.post("/create")                       #changed api
async def create_user(request: Request,
    username: str = Body(...),
  email: str = Body(...),
    password: str = Body(...),
    age: int = Body(...)
):
    try:
        data = await request.json()
    except ValueError:
        return {
            "status_code": 400,
            "description": "Invalid JSON format",
            "status": False,
            "data": [],
        }

    required_fields = [ "username", "email", "password", "age"]
    if not all(field in data for field in required_fields):
        return {
            "status_code": 400,
            "description": "Missing required fields",
            "status": False,
            "data": [],
        }

   
    if User.objects(username=data["username"]).first():
        return {
            "status_code": 400,
            "description": "Username already exists",
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
            "error": str(e),
        }

    access_token = create_access_token({"email": new_user.email})

    
    new_user.access_token = access_token
    new_user.save()

    user_data = new_user.to_mongo().to_dict()
    user_data["_id"] = str(user_data["_id"])

    return {
        "status_code": 200,
        "description": "User created successfully",
        "status": True,
        "access_token": access_token,
        "data": user_data
    }

@router.post("/update")                    #changed email
async def update_user(request: Request,
    user_id: str = Body(...),
    username: str = Body(None),
    password: str = Body(None),
    age: int = Body(None),
):
    try:
        
        user = User.objects(id=user_id).first()


        if not user:
            return {
                "status_code": 404,
                "description": "User not found",
                "status": False,
                "data": []
            }

        
        update_data = {}
        if username:
            update_data["set__username"] = username
        if password:
            update_data["set__password"] = password
        if age is not None:
            update_data["set__age"] = age

        if not update_data:
            return {
                "status_code": 400,
                "description": "No valid fields to update",
                "status": False
            }

      
        user.update(**update_data)
        user.reload()  

        return {
            "status_code": 200,
            "description": "User updated successfully",
            "status": True,
        }

    except Exception as e:
        return {
            "status_code": 500,
            "description": f"Error updating user: {str(e)}",
            "status": False
        }
   




@router.delete("/users")
async def delete_user(request: Request, user_id: str = Body(..., embed=True)):  
    try:
        user = User.objects(id=user_id).first()


        if not user:
            return {
                "status_code": 404,
                "description": "User not found",
                "status": False
            }

        user.delete()
        return {
            "status_code": 200,
            "description": "User deleted successfully",
            "status": True
        }
    except Exception as e:
        return {
            "status_code": 500,
            "description": f"Error deleting user: {str(e)}",
            "status": False
        }





@router.post("/list")
async def list_users(request: Request):
    try:
    
       
        users = list(User.objects.all())  

        user_list = []
        for user in users:
            user_data = user.to_mongo()  
            user_data["_id"] = str(user_data["_id"])  
            user_list.append(user_data)

        return {
            "status_code": 200,
            "description": "listed successfully",
            "status": True,
            "data": user_list
}

    except Exception as e:
        return {
            "status_code": 500,
            "description": f"Error listing user: {str(e)}",
            "status": False
        }

from fastapi import APIRouter,Body
from models import User
from mongoengine import connect,Document,StringField,IntField,DoesNotExist

router = APIRouter()


@router.post("/users/")
def create_user(
    username: str = Body(..., embed=True),
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    age: int = Body(..., embed=True),
):
    try:    
        if User.objects(email=email).first():
            return {
            "status_code": 400,
            "description": "User with this email already exists",
            "status": False,
            "data": []
        }
    
        new_user = User(username=username, email=email, password=password, age=age)
        new_user.save()

        return {
        "status_code": 200,
        "description": "User created successfully",
        "status": True,
        "data": [new_user.to_mongo().to_dict()]
    }
    except DoesNotExist:
        return {
            "status_code": 404,
            "description": "User not found",
            "status": False,
            "data": []
        }


@router.post("/update")
def update_user(user_id: str = Body(..., embed=True),
    username: str = Body(None, embed=True),
    password: str = Body(None, embed=True),
    age: int = Body(None, embed=True),
    email: str =Body(None, embed=True),
):
    try:
        existing_user = User.objects(id=user_id).first()


        update_data = {}
        if username: update_data["username"] = username
        if password: update_data["password"] = password
        if age: update_data["age"] = age
        if email:update_data["email"] = email

        existing_user.update(**update_data)

        return {
            "status_code": 200,
            "description": "User updated successfully",
            "status": True,
            "data": []
        }
    except DoesNotExist:
        return {
            "status_code": 404,
            "description": "User not found",
            "status": False,
            "data": []
        }







@router.delete("/users/{email}")
def delete_user(email: str):
    try:
        user = User.objects(email=email).first()
        user.delete()
        return {
            "status_code": 200,
            "description": "User deleted successfully",
            "status": True,
            "data": []
        }
    except DoesNotExist:
        return {
            "status_code": 404,
            "description": "User not found",
            "status": False,
            "data": []
        }



@router.get("/users/")
def list_users():
    try:

        users = User.objects().exclude("id")
        return {
            "status_code": 200,
            "description": "Users retrieved successfully",
            "status": True,
            "data": [user.to_mongo().to_dict() for user in users]
        }
    except DoesNotExist:
        return {
            "status_code": 404,
            "description": "User not found",
            "status": False,
            "data": []
        }


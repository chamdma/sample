from fastapi import FastAPI,Body
from mongoengine import connect,Document,StringField,IntField,DoesNotExist
app = FastAPI()


MONGO_URI ="mongodb+srv://chandanachandran3158:chandana33@cluster0.oz7fv.mongodb.net/User?retryWrites=true&w=majority&appName=Cluster0"

try:
    connect(host=MONGO_URI)
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("MongoDB Connection Failed:", str(e))






class User(Document):
    username = StringField(required=True)
    email = StringField(required=True,)
    password = StringField(required=True)
    age = IntField(required=True)


@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


@app.post("/users/")
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


@app.post("/users/update/{email}")
def update_user(email: str, username: str = None, password: str = None, age: int = None):
    try:
        existing_user = User.objects(email=email).first()
        update_data = {}
        if username: update_data["username"] = username
        if password: update_data["password"] = password
        if age: update_data["age"] = age
        existing_user.update(update_data)
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







@app.delete("/users/{email}")
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



@app.get("/users/")
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

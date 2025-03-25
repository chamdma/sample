from mongoengine import Document, StringField, IntField, connect


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


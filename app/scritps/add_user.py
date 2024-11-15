from app.database import db

def add_user():
    user_collection = db["users"]
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "hashed_password",
        "role": "user"
    }
    user_collection.insert_one(user_data)
    print("User added successfully!")

if __name__ == "__main__":
    add_user()

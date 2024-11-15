USER AUTHENTICATION SYSTEM

As per the assignment it uses a simple JWT-based authentication system using FastAPI and MongoDB. It includes role-based control (RBAC) where different entities such as administrators and users can access certain content. Authentication.
Role-Based Access Control (RBAC): Only users with administrator roles can access certain important details such as viewing all users' information.
Pydantic: Used for data analysis using Python type annotations. > Python Dotenv: Used to load environment variables. Run the native application:

1. Clone the repository
bash
Copy the code
git clone
cd
Create a virtual environment (optional, but recommended)
bash< br> Copy the code
python -m venv venv
source venv/bin/activate # Windows usage: venv\Scripts\activate
3 install -rrequirements.txt
4. Set environment variables
Create a .env file in the project root and add the following content:
makefile
Copy the code
MONGO_URI=mongodb ://your_mongo_uri
JWT_SECRET_KEY= your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=3600 # Timeout (in seconds)
5.
Your FastAPI application should now be running at http://localhost:8000. >Endpoint
1. POST /auth/register
Purpose: Register new users. : "string",
"password": "string",
"role": "admin/user" # Optional. Default is "User"
2. "password": "string"

Answer: Return an access_token that should be included in the authorization header of the next request. GET /users/all (admin only)
Purpose: Get all users in the system (accessible only to users with the administrator role). Answer: A group of users in the system. GET /users/me
Purpose: Get detailed information about logged in users. >5. PUT /users/update
Purpose: Update the content of logged in users. br > "Username": "New User",
"Email": "New Email"

DELETE /users/delete
Purpose: Delete the entry for the user account. Some of them are based on user roles:

User roles (users):
can access and modify their own content. Administrator's role (Admin):
Many user files from /users/all. For example:

Registered users. > Logs can be seen in the console where the FastAPI application is running. br>python
copy code from app.database
import db

def add_user():
user_collection = db["users"]
user_data = {
"Username": "newuser",
"Email": "newuser@example.com",
"Password": "hashed_password",
"Role": "person"

user_collection .insert_one(user_data)
print("User added successfully!")

if __name__ == "__main__":
add_user()


This script adds a new user for users who type in MongoDB. You can use MongoDB Atlas as a free cloud database. Keep it secure and do not expose it to public databases. It can be easily extended with further work or deployed to cloud platforms like AWS Lambda, Heroku or Vercel.

from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from models import Gender, Role, UpdateUserRequest, User

app = FastAPI()

db: List[User] = [
    User(
        # id = uuid4(),
        id = UUID("f4b20df0-1099-435a-a46c-79d083cb5b0d"),
        first_name = "Khoa",
        last_name = "Nguyen",
        gender = Gender.male,
        roles = [Role.student]
    ),
    User(
        # id = uuid4(),
        id = UUID("8db4f49e-77ea-414a-a94a-ce1dc493ef8a"),
        first_name = "Jennifer",
        last_name = "Tran",
        gender = Gender.female,
        roles = [Role.admin, Role.user]
    )
]

# Home 
@app.get("/")
async def root():
    return {"Hello": "Khoa"}

# Get request for users
@app.get("/users")
async def fetch_users():
    return db;

# Post request to add a new user
@app.post("/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

# Delete a user 
@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code = 404,
        detail = f"Sorry, user with id: {user_id} does not exsits"
    )

# Update user
@app.put("/users/{user_id}")
async def update_user(user_update: UpdateUserRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return user
    raise HTTPException(
        status_code = 404,
        detail = f"Sorry, user with id: {user_id} does not exists"
    )  
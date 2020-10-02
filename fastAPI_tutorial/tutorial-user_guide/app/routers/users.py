"""API Router"""
from fastapi import APIRouter

# import it and create an "instance" 
# the same way you would 
# with the class `FastAPI`
router = APIRouter()
# In this example, the variable is called `router`, 
# but you can name it however you want.

## Path operations with `APIRouter`
# Use it the same way you would use the `FastAPI` class
@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

# You can think of APIRouter as a "mini FastAPI" class.
    # All the same options are supported.
    # All the same parameters, responses, dependencies, tags, etc.

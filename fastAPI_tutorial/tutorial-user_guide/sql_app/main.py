"""Main FastAPI app"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
# when using the dependency in a path operation function, 
    # we declare it with the type `Session` 
    # This will then give us better editor support inside the path operation function, 
        # because the editor will know that the `db` parameter is of type `Session`

# Technical Details
    # The parameter `db` is actually of type `SessionLocal`, 
        # but this class 
            # (created with `sessionmaker()`) 
            # is a "proxy" of a SQLAlchemy `Session`, 
        # so, the editor 
            # doesn't really know what methods are provided.
    # But by declaring the type as `Session`, 
        # the editor now can know the available methods 
            # `.add()` 
            # `.query()` 
            # `.commit()`
            # etc 
        # and can provide better support (like completion). 
    # The type declaration doesn't affect the actual object.

from . import crud, models, schemas
from .database import SessionLocal, engine

## Create the database tables
# In a very simplistic way create the database tables:
models.Base.metadata.create_all(bind=engine)
## Alembic Note
    # Normally you would probably use Alembic 
        # to initialize your database 
            # (create tables, etc)
        # for "migrations" (THAT'S ITS MAIN JOB).
            # A "migration" is the set of steps needed whenever you change the structure
            # of your SQLAlchemy models, add a new attribute, etc. to replicate those 
            # changes in the database, add a new column, a new table, etc.
    # You can find an example of Alembic in a FastAPI project in the templates from 
        # "Project Generation - Template". 
        # Specifically in the `alembic` directory in the source code.


app = FastAPI()


# We need to have an 
    # independent database session/connection (`SessionLocal`) per request,
        # use the same session through all the request and 
        # then close it after the request is finished.
    # And then a new session will be created for the next request.
# For that, we will create a new dependency with `yield`, 
    # as explained before in the section about "Dependencies with yield".
# Dependency
def get_db():
    # `SessionLocal` class we created in the `sql_app/databases.py` 
    db = SessionLocal()
    # Our dependency will create a new SQLAlchemy `SessionLocal` 
    try:
        # that will be used in a single request,
        yield db
    finally:
        # and then close it once the request is finished.
        db.close()
# Info
    # We put the creation of the `SessionLocal()` 
        # and handling of the requests in a `try` block.
        # And then we close it in the `finally` block.
    # This way we make sure the 
        # database session is always closed after the request. 
        # Even if there was an exception while processing the request.
            # But you can't raise another exception from the exit code (after yield). 
    # See more in "Dependencies with yield" and "HTTPException"


# standard FastAPI path operations code.
    # We are creating the database session 
        # before each request 
        #    in the dependency with yield, 
        # and then closing it afterwards.
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, 
                db: Session = Depends(get_db)
                # And then we can create the required dependency 
                    # in the path operation function, 
                    # to get that session directly.
                ):
    db_user = crud.get_user_by_email(db, email=user.email)
    # With that, we can just 
        # call `crud.get_user` directly from inside of the path operation function 
        # and use that session.
        
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

    # Notice that the values you return are SQLAlchemy models, 
    # or lists of SQLAlchemy models.
@app.get("/users/", 
         response_model=List[schemas.User]
         # But as all the path operations have 
             # a `response_model` with Pydantic models / schemas using `orm_mode`,
         # the data declared in your Pydantic models will be 
             # extracted from them 
             # and returned to the client, 
             # with all the normal filtering and validation.
         )
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
    # Note: SQLAlchemy doesn't have compatibility for using `await` directly
    # => no `async def`

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
        ):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

## Migrations
# Because we are using SQLAlchemy directly 
# and we don't require any kind of plug-in for it to work with FastAPI, 
# we could integrate database migrations with Alembic directly.

# as the code related to SQLAlchemy and the SQLAlchemy models lives in separate independent files, 
    # you would even be able to perform the migrations with Alembic 
        # without having to install FastAPI, Pydantic, or anything else.

# The same way, you would be able 
# to use the same SQLAlchemy models and utilities 
    # in other parts of your code that are not related to FastAPI.
        # For example, in a background task worker with Celery, RQ, or ARQ.

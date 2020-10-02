"""CRUD utils"""
# Reusable functions to interact with the data in the database.
# in this example we are only creating and reading.

from sqlalchemy.orm import Session
#  allows you to declare the type of the db parameters 
#  and have better type checks and completion in your functions.

from . import models, schemas

# Tip
    # By creating functions that are 
        # independent of your path operation function, 
        # only dedicated to interacting with the database 
            # (get a user or an item)
    # you can more easily 
        # reuse them in multiple parts and 
        # also add unit tests for them.
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
    # Note: SQLAlchemy doesn't have compatibility for using `await` directly
    # => no `async def`

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    # Tip
        # The SQLAlchemy model for `User` 
            # contains a `hashed_password` that
            # should contain a secure hashed version of the password.
        # But as what the API client provides is the original password, you need to 
            # extract it and 
            # generate the hashed password in your application.
            # And then pass the `hashed_password` argument with the value to save.
    
    # Create a SQLAlchemy model instance with your data.
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    
    # `add` that instance object to your database session.
    db.add(db_user)

    # `commit` the changes to the database (so that they are saved).
    db.commit()

    # `refresh` your instance 
    # (so that it contains any new data from the database, 
    # like the generated ID).
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    # Create a SQLAlchemy model instance with your data.
    db_item = models.Item(**item.dict(), owner_id=user_id)
   
    # `add` that instance object to your database session.
    db.add(db_item)
    
    # `commit` the changes to the database (so that they are saved).
    db.commit()
    
    # `refresh` your instance 
        # (so that it contains any new data from the database, 
        # like the generated ID).
    db.refresh(db_item)
    return db_item

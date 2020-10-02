"""Create the database models"""
## SQLAlchemy style and Pydantic style
    # Notice that SQLAlchemy models 
        # define attributes using `=`, and 
        # pass the type as a parameter to Column, like in:
            # `name = Column(String)`
    # while Pydantic models 
        # declare the types using :, the new type annotation syntax/type hints:
            # `name: str`
    # Have it in mind, so you don't get confused when using `=` and `:` with them.

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship
# This will become, more or less, a "magic" attribute that 
# will contain the values from other tables related to this one.

from .database import Base

## Create SQLAlchemy `models` from the `Base` class
# These classes are the SQLAlchemy `models`.
class User(Base):
    __tablename__ = "users"
    # __tablename__ attribute tells SQLAlchemy 
    # the name of the table to use in the database for each of these models.

    ## Create model attributes/columns
    # Now create all the model (class) attributes.
        # Each of these attributes represents a column in its corresponding database table.
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # We use `Column` from SQLAlchemy as the default value.
        # And we pass a SQLAlchemy class "type" 
            # that defines the type in the database, as an argument.
                # Integer 
                # String
                # Boolean 

    items = relationship("Item", back_populates="owner")
    # When accessing the attribute `items` in a `User`, 
       # as in `my_user.items`, 
    # it will have a list of `Item` SQLAlchemy models 
      # (from the `items` table) 
    # that have a foreign key pointing to this record in the `users` table.
    
    # When you access `my_user.items`, 
        # SQLAlchemy will actually go and fetch the items from the database in the
        # `items` table and populate them here.

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    # when accessing the attribute `owner` in an `Item`, it will contain a 
    # `User` SQLAlchemy model from the `users` table. It will use the `owner_id` 
    # attribute/column with its foreign key to know which record to get from
    # the `users` table.
    
# Tip
    # SQLAlchemy uses the term "model" to refer to 
        # classes and instances that interact with the database.
    # But Pydantic also uses the term "model" to refer to something different, the 
        # data validation, 
        # conversion, and 
        # documentation classes and instances.

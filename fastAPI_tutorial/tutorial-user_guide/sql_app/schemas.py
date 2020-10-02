"""Create the Pydantic models"""
## SQLAlchemy style and Pydantic style
    # Notice that SQLAlchemy models 
        # define attributes using `=`, and 
        # pass the type as a parameter to Column, like in:
            # `name = Column(String)`
    # while Pydantic models 
        # declare the types using :, the new type annotation syntax/type hints:
            # `name: str`
    # Have it in mind, so you don't get confused when using `=` and `:` with them.


from typing import List, Optional

from pydantic import BaseModel
# Pydantic models as "schemas"

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

# before creating an item, we don't know what will be the ID assigned to it, 
class ItemCreate(ItemBase):
    pass


# but we will already know its ID when reading it (when returning it from the API) 
class Item(ItemBase):
    id: int
    owner_id: int

    # Internal `Config` class.
    # This `Config` class is used to provide configurations to Pydantic.
    class Config:
        orm_mode = True
    # Pydantic's `orm_mode` will tell the Pydantic model 
        # to read the data even if it is not a dict, 
        # but an ORM model (or any other arbitrary object with attributes).
    # This way, 
        # instead of only trying to get the id value from a dict, as in:
            # `id = data["id"]`
        # it will also try to get it from an attribute, as in:
            # `id = data.id`
        # And with this, the Pydantic model is compatible with ORMs, and 
            # you can just declare it in the `response_model` argument in your path operations.
    # You will be able to return a database model and it will read the data from it.


class UserBase(BaseModel):
    email: str

# for security, the `password` WON'T be in other Pydantic models, 
    # for example, it won't be sent from the API when reading a user.
class UserCreate(UserBase):
    password: str


# when reading a user, we can now declare that items will contain the items that belong to this user.
    # Not only the IDs of those items, 
    # but all the data that we defined in the Pydantic model for reading items:`Item`.
class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []
    # Tip
        # Notice that `User`, 
            # the Pydantic model that will be used when reading a user 
            # (returning it from the API) 
        # doesn't include the password.

    class Config:
        orm_mode = True
    ## Technical Details about ORM mode
        # SQLAlchemy and many others are by default "lazy loading".
            # they don't fetch the data for relationships from the database 
            # unless you try to access the attribute that would contain that data.
        # For example, accessing the attribute items: `current_user.items`
            # would make SQLAlchemy go to the `items` table and 
            # get the items for this user, BUT NOT BEFORE.
        # Without `orm_mode`, if you returned a SQLAlchemy model from your path operation, 
            # it wouldn't include the relationship data. 
            # Even if you declared those relationships in your Pydantic models.
        # But with ORM mode, 
            # as Pydantic itself will try to access the data it needs from attributes
                # (instead of assuming a dict), 
            # you can declare the specific data you want to return and 
                # it will be able to go and get it, even from ORMs.    
        
        


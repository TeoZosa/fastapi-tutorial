"""FastAPI intro user guide"""

"""Query Parameters"""
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_user_item(
    # (PATH parameters)
    item_id: str,  # required
    # (QUERY parameters) e.g.
        # http://127.0.0.1:8000/items/foo-item?needy=sooooneedy&skip=0
        # ===
        # http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
    needy: str,  # required (no default value)
    skip: int = 0, # optional w/ default value
    limit: Optional[int] = None, #optional NO default value (MUST be int, if specified)
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

"""Request Body"""
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


# Pydantic data model: request/response bodies
# auto validation
# auto parsing: Set intersection of fields (i.e. input_model ⋂ output_model)
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()

#You can also declare body, path and query parameters, all at the same time.
# FastAPI will recognize each of them and take the data from the correct place.


@app.put("/items/{item_id}")
async def create_item(
        # PATH parameter
        # If the parameter is also declared in the path, it will be used as a path parameter.
        item_id: int, 
        # REQUEST body
        # If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
        item: Item, 
        # QUERY (q as a convention for remainder query string)
        # If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
        q: Optional[str] = None # None value => optional
        
        ):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
"""Query Parameters and String Validations"""
from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
        q: Optional[str] = Query(
                None,
                # alias is what will be used to find the parameter value
                #i.e. since `item-query` is not a valid python variable name
                alias="item-query",
                
                # Metadata
                # included in generated OpenAPI and used by the 
                # documentation user interfaces and external tools.
                title="Query string",
                description="Query string for the items to search in the database that have a good match",

                # Input validation (string)
                min_length=3,
                max_length=50,
                regex="^fixedquery$",
                
                # Add deprecation notice to docs for clients 
                deprecated=True,
                )
        ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""Path Parameters and Numeric Validations"""
from fastapi import FastAPI, Path, Query

app = FastAPI()

# 
# And you can also declare numeric validations:
# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal
@app.get("/items/{item_id}")
async def read_items(
        
        # If you want to 
        # declare the q query parameter without a Query nor any default value, 
        # and the path parameter item_id using Path, 
        # and have them in a different order,
        # =>
        # Pass *, as the first parameter of the function.
        *,
        # Python won't do anything with that *, but it will know that 
        # all the following parameters should be called as keyword arguments (key-value pairs), also known as kwargs. 
        # Even if they don't have a default value.
        
        item_id: int = Path(
                            # A path parameter is always required as it has 
                            # to be part of the path.
                            # So, you should declare it with `...` to mark it as required.
                            # 
                            ...,
                            # Nevertheless, even if you declared it with None or set a 
                            # default value, it would not affect anything, it would 
                            # still be always required. 
                            
                            #metadata
                            # With Query, Path (and others you haven't seen yet) 
                            # you can declare metadata and string validations in the same ways as with Query Parameters and String Validations.
                            title="The ID of the item to get", 
            
                            # Input validation (numeric)
                            ge=0, le=1000),
        # QUERY parameters
        q: str, # REQUIRED (no default value)
        
        # REQUIRED (`...` input === no default value)
        size: float = Query(..., # ; to make optional => None
                            gt=0, lt=10.5) 
        ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

"""Body - Multiple Parameters"""

from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/items/{item_id}")
async def update_item(
        *,
        item_id: int,
        
        #multiple body parameters
        # FastAPI will notice that there are more than one body parameters in the function (two parameters that are Pydantic models).
        #b1
        item: Item,
        #b2
        user: User,
        # b3 (singular)  # instruct FastAPI to treat it as another body key using `Body`
        importance: int = Body(..., gt=0),
        # So, it will then use the parameter names as keys (field names) in the body, and expect a body like:
        # `
        #  {
        #         "item": {
        #                 "name": "Foo",
        #                 "description": "The pretender",
        #                 "price": 42.0,
        #                 "tax": 3.2
        #                 },
        #         "user": {
        #                 "username": "dave",
        #                 "full_name": "Dave Grohl"
        #                 },
        #         "importance": 5
        #         }
        # `

        q: Optional[str] = None
        ):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

## Embed a single body parameter
# e.g. {
#         "body_param": {
#                 ...
#                 }
#         }
# instead of
# {
#       ...
#         }
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int,
                      #embed key as inner key of a singleton dict                      
                      item: Item = Body(..., embed=True)):
                      # i.e., 
                      # {
                      #         "item": {
                      #                 "name": "Foo",
                      #                 "description": "The pretender",
                      #                 "price": 42.0,
                      #                 "tax": 3.2
                      #                 }
                      #         }
                      # instead of
                      # {
                      #         "name": "Foo",
                      #         "description": "The pretender",
                      #         "price": 42.0,
                      #         "tax": 3.2
                      #         }
    results = {"item_id": item_id, "item": item}
    return results

"""Body - Fields"""
from typing import Optional

from fastapi import Body, FastAPI
#NOTE!: `Field` imported from pydantic!
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    
    # Metadata/validation on data model attributes
    description: Optional[str] = Field(
            None, # optional
            # Metadata
            title="The description of the item",
            # Input validation (string) 
            max_length=300
            )
    price: float = Field(
            ..., # REQUIRED
            # Input validation (numeric) 
            gt=0, 
            # Metadata
            description="The price must be greater than zero")
    
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

"""Body - Nested Models"""
# Set types
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    # With this, even if you receive a request with duplicate data, 
    # it will be converted to a set of unique items.
    # 
    # And whenever you output that data, even if the source had duplicates, 
    # it will be output as a set of unique items.
    tags: Set[str] = set()
    # And it will be annotated / documented accordingly too.


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# Special types and validation
# Deeply nested models
from typing import List, Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl # special type for validation
# other [pydantic custom types](https://pydantic-docs.helpmanual.io/usage/types/) 

app = FastAPI()


class Image(BaseModel):
    # The string will be checked to be a valid URL, and 
    # documented in JSON Schema / OpenAPI as such.
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    images: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

# This will expect (convert, validate, document, etc) a JSON body like:
# `
# {
#         "name": "OFFERNAME",
#         "description": "OFFER DESCRIPTION",
#         "price": 42.0,
#         "items": [
#           {
#             "name": "Foo",
#             "description": "The pretender",
#             "price": 42.0,
#             "tax": 3.2,
#             "tags": [
#                     "rock",
#                     "metal",
#                     "bar"
#                     ],
#             "images": [
#                     {
#                             "url": "http://example.com/baz.jpg",
#                             "name": "The Foo live"
#                             },
#                     {
#                             "url": "http://example.com/dave.jpg",
#                             "name": "The Baz"
#                             }
#                     ]
#               }
#           }
# `


# Bodies of arbitrary dicts
from typing import Dict

from fastapi import FastAPI

app = FastAPI()

# You can also declare a body as a dict with keys of some type and values of other type.
# Without having to know beforehand what are the valid field/attribute names 
# (as would be the case with Pydantic models).
# 
# This would be useful if you want to receive keys that you don't already know.
# Other useful case is when you want to have non-str keys, e.g. int.

@app.post("/index-weights/")
async def create_index_weights(
        # In this case, you would accept any dict 
        # as long as it has int keys with float values
        weights: Dict[int, float]):
    return weights
# Note: JSON *only supports str as keys*.
# But Pydantic has automatic data conversion.
#   => even though your API clients can only send strings as keys, 
#   as long as those strings contain pure integers, 
#   Pydantic will convert them and validate them.
#   And the dict you receive as weights will actually have int keys and float values.



"""Schema Extra - Example"""
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    # Declare an example for a Pydantic model using `Config` and `schema_extra`, 
    # as described in Pydantic's docs: Schema customization
    class Config:
        schema_extra = {
                "example": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                        }
                }
    # That extra info will be added as-is to the output JSON 
    # Schema.

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

## Field additional arguments
## Body additional arguments
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    # equivalent to setting a single data structure in the `example` param 
    # of the `Body` class function
    name: str
    # name: str = Field(..., example="Foo")
    description: Optional[str] = None
    # description: Optional[str] = Field(None, example="A very nice Item").
    
    price: float
    tax: Optional[float] = None

@app.put("/items/{item_id}")
async def update_item(
        item_id: int,
        item: Item = Body(
                ...,
                # extra arguments passed won't add any validation,
                # only annotation, for documentation purposes.
                example={ 
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                        },
                #equivalent to setting it in the Field class function
                
                ),
        ):
    results = {"item_id": item_id, "item": item}
    return results

#     i.e.
# Request body
# Example Value Schema
# `
#     {
#             "name": "Foo",
#             "description": "A very nice Item",
#             "price": 35.4,
#             "tax": 3.2
#             }
# `

# NOTE!
# Technical Details
# About `example` vs `examples`...
# JSON Schema defines a field `examples` in the most recent versions, 
# but OpenAPI is based on an older version of JSON Schema that didn't have examples.
# 
# So, OpenAPI defined its own `example` for the same purpose 
# (as `example`, not `examples`), and that's what is used by the docs UI (using Swagger UI).
# So, although example is not part of JSON Schema, 
# it is part of OpenAPI, and that's what will be used by the docs UI.

# Other info
# The same way, you could add your own custom extra info 
# that would be added to the JSON Schema for each model, 
# for example to customize a frontend user interface, etc.

"""Extra Data Types"""
from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID
from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
        item_id: UUID,
        # standard "Universally Unique Identifier", 
        # common as an ID in many databases and systems.
        # In requests and responses 
        # will be represented as a str
        
        start_datetime: Optional[datetime] = Body(None),
        end_datetime: Optional[datetime] = Body(None),
        # In requests and responses 
        # will be represented as a str in ISO 8601 format, 
        # like: 2008-09-15T15:53:00+05:00.
        
        repeat_at: Optional[time] = Body(None),
        # In requests and responses 
        # will be represented as a str in ISO 8601 format, 
        # like: 14:23:55.003.
        
        process_after: Optional[timedelta] = Body(None),
        # In requests and responses 
        # will be represented as a float of total seconds.
        # Pydantic also allows representing it as a 
        # "ISO 8601 time diff encoding", see the docs for more info.
        ):
    
    # Perform `datetime` operations 
    # (auto-conversion of str parameters to Python types)
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
            "item_id": item_id,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "repeat_at": repeat_at,
            "process_after": process_after,
            "start_process": start_process,
            "duration": duration,
            }
## Other examples:

s = frozenset
# In requests and responses, 
# treated the same as a set:
# In requests, 
#   a list will be read, eliminating duplicates and converting it to a set.
# In responses, 
#   the set will be converted to a list.
# The generated schema will specify that the set values are unique 
# (using JSON Schema's uniqueItems).

b = bytes
# In requests and responses 
# will be treated as str.
# The generated schema will specify that it's a str with binary "format".

from decimal import Decimal
d = Decimal(1)
# In requests and responses, 
# handled the same as a float.

"""Cookie Parameters"""
from typing import Optional

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(
        # Same pattern as `Path`, `Query`, etc.
        ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

"""Header Parameters"""
## Automatic conversion
from typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()

#tl;dr: `-` converted to `_` automatically. 

# Header has a little extra functionality on top of what Path, Query and Cookie provide.
# 
# Most of the standard headers are separated by a "hyphen" character, 
# also known as the "minus symbol" (-).
# 
# But a variable like `user-agent` is invalid in Python.
# So, by default, 
# Header will convert the parameter names characters 
# from underscore (_) to hyphen (-) to extract and document the headers.
# 
# Also, HTTP headers are case-insensitive, so, 
# you can declare them with standard Python style (also known as "snake_case").
# 
# So, you can use `user_agent` as you normally would in Python code, 
# instead of needing to capitalize the first letters as `User_Agent` or something similar.
@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

## Disable automatic conversion
from typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
        # If for some reason you need 
        # to disable automatic conversion of underscores to hyphens, 
        # set the parameter `convert_underscores` of Header to False:
        strange_header: Optional[str] = Header(None, convert_underscores=False)
        ):
    return {"strange_header": strange_header}
# WARNING:
# Before setting convert_underscores to False, bear in mind that 
# some HTTP proxies and servers disallow the usage of headers with underscores.

## Duplicate headers
from typing import List, Optional

from fastapi import FastAPI, Header

app = FastAPI()

# It is possible to receive duplicate headers. That means, 
# the same header with multiple values.
# 
# You can define those cases using a 
# list in the type declaration.
# 
# You will receive all the values 
# from the duplicate header as a Python list.
# 
# For example, 
# to declare a header of X-Token 
# that can appear more than once, 
# you can write:
@app.get("/items/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}
# If you communicate with that path operation sending two HTTP headers like:
# X-Token: foo
# X-Token: bar
# 
# The response would be like:
# {
#     "X-Token values": [
#         "bar",
#         "foo"
#     ]
# }
"""Response model"""
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []

# You can declare the model used for the response 
# with the parameter `response_model` in any of the path operations:
# @app.get()
# @app.post()
# @app.put()
# @app.delete()
# etc.
@app.post("/items/", response_model=Item)
# Will limit the output data to that of the model. 
async def create_item(item: Item):
    return item

## Limit Output Data
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

# FastAPI will take care of filtering out all the data 
# that is not declared in the output model (using Pydantic).
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

# ...we declared the response_model to be our model UserOut, that 
# doesn't include the password:
@app.post("/user/", response_model=UserOut)
# Here, even though our path operation function is returning 
# the same input user that contains the password
async def create_user(user: UserIn):
    return user


## Response model encoding parameters
from typing import List, Optional
 
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    # Default params
    description: Optional[str] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
        "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
        }

@app.get("/items/{item_id}", response_model=Item,
         # default values won't be included in the response, 
         # only the values actually set.
         response_model_exclude_unset=True
         # Can also use:
         #   response_model_exclude_defaults=True
         #   response_model_exclude_none=True
         )

async def read_item(item_id: str):
    return items[item_id]

# the response will EXCLUDE UNSET VALUES

# for the item with ID foo,
# {
#     "name": "Foo",
#     "price": 50.2
# }

# if your DATA HAS VALUES FOR THE MODEL'S FIELDS WITH DEFAULT VALUES, 
# they will be included in the response.
# 
# like the item with ID bar:
# {
#     "name": "Bar",
#     "description": "The bartenders", #<= different
#     "price": 62,
#     "tax": 20.2 #<= different
# }

# If the DATA HAS THE SAME VALUES AS THE DEFAULT ONES, 
# they will be included in the JSON response.
# 
# like the item with ID baz:
# {
#     "name": "Baz",
#     "description": None, # <= same
#     "price": 50.2,
#     "tax": 10.5, # <= same
#     "tags": [] # <= same
# }
# FastAPI is smart enough (actually, Pydantic is smart enough) to realize 
# that, even though description, tax, and tags have the same values as the 
# defaults, they were set explicitly (instead of taken from the defaults).

## response_model_include and response_model_exclude
# 
# This can be used as a quick shortcut if you have only one Pydantic model 
# and want to remove some data from the output.

# STILL RECOMMENDED TO USE MULTIPLE CLASSES INSTEAD OF THESE PARAMETERS.
#   This is because the JSON Schema generated in your app's OpenAPI (and the 
#   docs) will still be the one for the complete model, even if you use 
#   response_model_include or response_model_exclude to omit some attributes.
#   
#   This also applies to response_model_by_alias that works similarly.


from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5


items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
        "baz": {
                "name": "Baz",
                "description": "There goes my baz",
                "price": 50.2,
                "tax": 10.5,
                },
        }


# You can also use the path operation decorator parameters 
# `response_model_include` and `response_model_exclude`.
@app.get("/items/{item_id}/name",
        response_model=Item,
        # They take a `set` of `str` with 
        # the name of the attributes to include (omitting the rest) 
        response_model_include={"name", "description"},
        )
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, 
         # exclude (including the rest).
         response_model_exclude=["tax"]
         # If you forget to use a `set` 
         # and use a `list` or `tuple` instead, 
         # FastAPI will still convert it to a `set` and it will work correctly
         )
async def read_item_public_data(item_id: str):
    return items[item_id]

"""Extra Models"""
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str
# == 
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Optional[str] = None

class UserOut(UserBase):
    pass
# == 
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Optional[str] = None


class UserInDB(UserBase):
    hashed_password: str
# == 
# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    # Unpack `user_in` dict and add new key/val pair
    user_in_db = UserInDB(
                          # built-in dictify method
                          **user_in.dict(), 
                          hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

## `Union` or `anyOf`
# You can declare a response 
# to be the Union of two types, 
#   that means, that the response would be any of the two.
# It will be defined in OpenAPI with `anyOf`.
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
        "item1": {"description": "All my friends drive a low rider", "type": "car"},
        "item2": {
                "description": "Music is my aeroplane, it's my aeroplane",
                "type": "plane",
                "size": 5,
                },
        }


@app.get("/items/{item_id}", 
         # When defining a Union, 
         # include the most specific type first, 
         # followed by the less specific type. 
         response_model=Union[PlaneItem, CarItem]
         # the more specific `PlaneItem` comes before `CarItem` 
         # in `Union[PlaneItem, CarItem]`.
         )
async def read_item(item_id: str):
    return items[item_id]

## List of models
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


items = [
        {"name": "Foo", "description": "There comes my hero"},
        {"name": "Red", "description": "It's my aeroplane"},
        ]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

## Response with arbitrary dict

# declare a response 
# using a plain arbitrary dict, 
# declaring just the type of the keys and values, 
# without using a Pydantic model.
#
# This is useful if 
# you don't know the valid field/attribute names 
# (that would be needed for a Pydantic model) beforehand.
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

"""Response Status Code"""
from fastapi import FastAPI, status

app = FastAPI()

# Returns status code in response
# Documents in OpenAPI schema
@app.post("/items/", 
          # Shortcut to remember the names
          #     You can use the convenience variables from `fastapi.status`.
          status_code=status.HTTP_201_CREATED,  # == `status_code=201`
          )
# `status_code` can alternatively also 
# receive an `IntEnum`, 
# such as Python's `http.HTTPStatus`.
async def create_item(name: str):
    return {"name": name}


# Some response codes indicate that the 
# response does not have a body.
# FastAPI knows this, and will produce OpenAPI docs that state there is no 
# response body.


# Note
# ≥100: "Information". 
    # Rarely use them directly. 
    # Responses CANNOT HAVE A BODY.

# ≥200: "Successful" . 
    # Ones you would use the most.
    # 200: "OK" 
        # default status code 
    # 201: "Created" 
        # commonly used after creating a new record in the database.
    # 204: "No Content" (special case) 
        # used when there is no content to return to the client,
        # and so the response must not have a body.

# ≥300: "Redirection". 
    # Responses may or may not have a body, 
    # 304: "Not Modified" (EXCEPTION) 
        # MUST NOT HAVE A BODY.

# ≥400: "Client error"  
    # second most-used type 
    # 404: "Not Found"
    # For generic errors from the client, 
    # you can just use 400.

# ≥500: server errors. 
    # almost never use them directly. 
    # When something goes wrong at some part in your application code, 
    # or server, it will automatically return one of these status codes.

"""Form Data"""
# For example, in 
# one of the ways the OAuth2 specification can be used 
# (called "password flow") it is 
# required to send a username and password 
# as form fields.

# The spec requires the fields to be 
# exactly named `username` and `password`, and to be 
# sent as form fields, not JSON.
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(
                # To declare form bodies, you need to use Form explicitly, because 
                # without it the parameters would be interpreted 
                # as query parameters or body (JSON) parameters.
                username: str = Form(...),
                # With Form you can declare the 
                # same metadata and validation 
                # as with Body (and Query, Path, Cookie).       
                password: str = Form(...)
        ):
    return {"username": username}
## About "Form Fields"
    # The way HTML forms (<form></form>) sends the data to the server normally 
    # uses a "special" encoding for that data, it's different from JSON.
    # 
    # FastAPI will make sure to read that data from the right place 
    # instead of JSON.

# Technical Details
    # Data from forms is normally encoded using the "media type" 
    # `application/x-www-form-urlencoded`
    # But when the form includes files, 
    # it is encoded as multipart/form-data. 

    # You'll read about handling files in the next chapter.
    # If you want to read more about these encodings and form fields, head to 
    # the MDN web docs for POST.

# Warning
    # can declare multiple Form parameters in a path operation, but you
    # can't also declare Body fields that you expect to receive as JSON, 
    # as the request will have the body encoded using
    # `application/x-www-form-urlencoded`
    # instead of `application/json`
    
    # This is not a limitation of FastAPI, it's part of the HTTP protocol.

"""Request Files"""
from typing import List

from fastapi import FastAPI, File, UploadFile
# `File` is a class that inherits directly from `Form`.

from fastapi.responses import HTMLResponse
# You could also use from starlette.responses import HTMLResponse.
# FastAPI provides the same starlette.responses as fastapi.responses 
# just as a convenience for you, the developer. 
# But most of the available responses come directly from Starlette.

app = FastAPI()


# It's possible to 
# upload several files at the same time.

# They would be associated to the same 
# "form field" sent using "form data".
# To use that, declare a `List` of bytes or `UploadFile`
@app.post("/files/")
async def create_files(
        # Create file parameters the same way you would for `Body` or `Form`:
        files: List[bytes] = File(...)
        # If you declare the type of your path operation function parameter as `bytes`, 
        # FastAPI will read the file for you and you will receive the contents as `bytes`.
            # the whole contents will be STORED IN MEMORY. 
            # This will work well for small files.
        ):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
        files: List[UploadFile] = File(...)
# UploadFile has several advantages over bytes:
    # It uses a "spooled" file:
        # A file stored in memory up to a maximum size limit, and 
        # after passing this limit it will be stored in disk.
        # This means that it will work well for large files 
        # like images, videos, large binaries, etc. 
        # without consuming all the memory.
    # You can get METADATA from the uploaded file.
    # It has a FILE-LIKE ASYNC INTERFACE.
    # It exposes an actual Python SpooledTemporaryFile object that you can 
    #   pass directly to other libraries that expect a FILE-LIKE OBJECT.
                                  ):
    return {"filenames": [file.filename for file in files]}
# Notice that, as of 2019-04-14, 
    # Swagger UI doesn't support 
    # multiple file uploads in the same form field. 
        # For more information, check #4276 and #3641.
# Nevertheless, FastAPI is already compatible with it, using the standard OpenAPI.
# So, whenever Swagger UI supports multi-file uploads, 
# or any other tools that supports OpenAPI, 
# they will be compatible with FastAPI.

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
# UploadFile has the following attributes:
    # `filename`: A str with the original file name that was uploaded (e.g. myimage.jpg).
    # `content_type`: A str with the content type (MIME type / media type) (e.g. image/jpeg).
    # `file`: A SpooledTemporaryFile (a file-like object). This is the actual Python file that you can pass directly to other functions or libraries that expect a "file-like" object.

# UploadFile has the following async methods. They all call the corresponding file methods underneath (using the internal SpooledTemporaryFile).
    # `write(data)`: Writes data (str or bytes) to the file.
    # `read(size)`: Reads size (int) bytes/characters of the file.
    # `seek(offset)`: Goes to the byte position offset (int) in the file.
    #       E.g., `await myfile.seek(0)` would go to the start of the file.
    #       This is especially useful if you run await `myfile.read()` once 
    #       and then need to read the contents again.
    # `close()`: Closes the file.

# As all these methods are async methods, you need to "await" them.
# For example, 
    # inside of an async path operation function 
    # you can get the contents with:
        # `contents = await myfile.read()`
    
    # If you are inside of a normal def path operation function, 
    # you can access the UploadFile.file directly, for example:
        # `contents = myfile.file.read()`

# async Technical Details
    # When you use the async methods, 
    # FastAPI runs the file methods in a threadpool 
    # and awaits for them.

# Starlette Technical Details
    # FastAPI's UploadFile inherits directly from Starlette's UploadFile, 
    # but adds some necessary parts to make it compatible with Pydantic 
    # and the other parts of FastAPI.

## What is "Form Data"

"""Request Forms and Files"""
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(
        file: bytes = File(...), 
        fileb: UploadFile = File(...), 
        token: str = Form(...)
        ):
    return {
            "file_size": len(file),
            "token": token,
            "fileb_content_type": fileb.content_type,
            }
# Warning
# You can declare multiple File and Form parameters in a path operation, but
# you CAN'T ALSO DECLARE BODY FIELDS THAT YOU EXPECT TO RECEIVE AS JSON, 
# as the request will have the body encoded using 
# `multipart/form-data` instead of `application/json`.

# This is not a limitation of FastAPI, it's part of the HTTP protocol.

"""Handling Errors"""
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, 
                            detail="Item not found",
                            # can pass any value that can be converted to JSON 
                            # as the parameter detail, not only str.
                            # You could pass a dict, a list, etc.
                            # They are handled automatically by FastAPI 
                            # and converted to JSON.

                            # Add custom headers to the HTTP error 
                            # (e.g. for some types of security)
                            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
# If the client requests http://example.com/items/foo 
# (an item_id "foo"), 
# that client will receive an HTTP status code of 200, 
# and a JSON response of:
# {
#   "item": "The Foo Wrestlers"
# }

# But if the client requests http://example.com/items/bar 
# (a non-existent item_id "bar"), 
# that client will receive an HTTP status code of 404 (the "not found" error),
# and a JSON response of:
# {
#   "detail": "Item not found"
# }

## Custom exception handlers
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
            status_code=418,
            content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
            )
    # you will receive a clean error, with an HTTP status code of 418 and a 
    # JSON content of:
    # {"message": "Oops! yolo did something. There goes a rainbow..."}


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    # Here, if you request /unicorns/yolo, 
    # the path operation will raise a UnicornException.
    if name == "yolo":
        raise UnicornException(name=name)
        # But it will be handled by the `unicorn_exception_handler`
    return {"unicorn_name": name}

## Override the HTTPException error handler
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # return a plain text response instead of JSON for these errors:
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

## Use the RequestValidationError body
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            
            content=jsonable_encoder({
                    # The `RequestValidationError` 
                    # contains the body it received with invalid data.
                    # use it while developing your app 
                    # to log the body and debug it, return it to the user, etc
                    "detail": exc.errors(), "body": exc.body}),
            )

class Item(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item

# Now try sending an invalid item like:
# {
#   "title": "towel",
#   "size": "XL"
# }

# You will receive a response telling you that the data is invalid 
# containing the received body:
# {
#   "detail": [
#     {
#       "loc": [
#         "body",
#         "size"
#       ],
#       "msg": "value is not a valid integer",
#       "type": "type_error.integer"
#     }
#   ],
#   "body": {
#     "title": "towel",
#     "size": "XL"
#   }
# }


# FastAPI's HTTPException vs Starlette's HTTPException
    # FastAPI has its own HTTPException.
        # And FastAPI's HTTPException error class inherits from Starlette's 
        # HTTPException error class.
    # The only difference, is that 
        # FastAPI's HTTPException allows you to 
        # add headers to be included in the response.
    # This is needed/used internally for OAuth 2.0 and some security utilities.
    
    # So, you can keep raising FastAPI's HTTPException as normally in your code.
        # But when you register an exception handler, you should register it for 
        #   Starlette's HTTPException.
        # This way, if any part of Starlette's internal code, or a Starlette 
        #   extension or plug-in, raises a Starlette HTTPException, 
        #   your handler will be able to catch and handle it.

## Re-use FastAPI's exception handlers
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    )
from fastapi.exceptions import RequestValidationError

# In this example, to be able to have both `HTTPExceptions` in the same code, 
# Starlette's exceptions is renamed to `StarletteHTTPException`:
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# You could also just want to use the exception somehow, 
# but then use the same default exception handlers from FastAPI.
# You can import and re-use the 
# default exception handlers from fastapi.exception_handlers:
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


"""Path Operation Configuration"""

## Tags
## Deprecate a path operation
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items/", 
          response_model=Item,

          # Add tags to your path operation, 
          # pass the parameter tags with a 
          # list of str (commonly just one str):
          tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


@app.get("/elements/", tags=["items"], 
         # Mark a path operation as deprecated, but without removing it
         deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]


## Summary and Description
## Description from docstring
## Response description
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items/", 
          response_model=Item, 
          summary="Create an item",
          
          # Specify PATH OPERATION description 
          # with plaintext
          #description="Create an item with all the information:",

          # Specify the RESPONSE description
          response_description="The created item",
          )

# Specify the PATH OPERATION description 
# with rich text (Markdown) via docstring 
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

"""JSON Compatible Encoder"""
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# Let's imagine that you have a database 
# that only receives JSON compatible data.
fake_db = {}
# For example, 
    # it doesn't receive datetime objects, as those are not compatible with JSON.
    # So, a datetime object 
    # would have to be converted to a str containing the data in ISO format.

    # The same way, 
    # this database wouldn't receive a Pydantic model (an object with attributes), 
    # only a dict.

# You can use jsonable_encoder for that.

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    # It receives an object, like a Pydantic model, 
    # and returns a JSON compatible version:
    json_compatible_item_data = jsonable_encoder(item)
    # In this example, it would 
        # convert the Pydantic model to a dict, 
        # and the datetime to a str.
    fake_db[id] = json_compatible_item_data
# Note: 
# It doesn't return a large str containing the data in JSON format (as a string). 
# It returns a Python standard data structure (e.g. a dict) 
# with values and sub-values that are all compatible with JSON.

"""Body - Updates"""
# Update replacing with PUT
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
        "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
        }


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    # REPLACEMENT
    items[item_id] = update_item_encoded
    return update_item_encoded
# WARNING about replacing¶
# That means that if you want to update the item bar using PUT with a body containing:
# {
#         "name": "Barz",
#         "price": 3,
#         "description": None,
#         }
# because it doesn't include the already stored attribute "tax": 20.2, 
# the input model would take the default value of "tax": 10.5.
# And the data would be saved with that "new" tax of 10.5.

## Partial updates with Patch
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
        "foo": {"name": "Foo", "price": 50.2},
        "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
        "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
        }


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

@app.patch("/items/{item_id}", response_model=Item)
# Note:
# PATCH is less commonly used and known than PUT.
    # And many teams use only PUT, even for partial updates.
    # You are free to use them however you want, FastAPI doesn't impose any restrictions.
# But this guide shows you, more or less, how they are INTENDED to be used.
    # You can actually use this same technique with an HTTP PUT operation.
    # But the example here uses PATCH because it was created for these use cases.
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    
    # Using Pydantic's exclude_unset parameter
    update_data = item.dict(exclude_unset=True)
    # If you want to receive partial updates, 
    # it's very useful to use the parameter 
    # `exclude_unset` in Pydantic's model's `.dict()`
    # That would generate a dict with 
        # only the data that was set when creating the item model, excluding default values.
    # Then you can use this to generate a dict 
    # with only the data that was set (sent in the request), 
    # omitting default values
    
    #Using Pydantic's update parameter
    updated_item = stored_item_model.copy(update=update_data)
    # Now, you can create a copy of the existing model using `.copy()`, 
    # and pass the update parameter with a dict containing the data to update.
    
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
# Notice that the input model is still validated.

# So, if you want to receive partial updates that can omit all the attributes, 
# you need to have a model with all the attributes marked as optional 
# (with default values or None).

# To distinguish from the models with all optional values for updates 
# and models with required values for creation, 
# you can use the ideas described in "Extra Models".

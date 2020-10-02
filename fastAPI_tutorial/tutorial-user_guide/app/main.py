"""The main FastAPI"""
# Here's where you import and use the class FastAPI.
# This will be the main file in your application that ties everything together.

from fastapi import Depends, FastAPI, Header, HTTPException

## Import the APIRouter

# But this time
# we are not adding path operations directly with the FastAPI app.
# We (relative) import the other submodules that have APIRouters:
from .routers import items, users
# Note: 
# As the file `app/routers/items.py` is part of the same Python package, 
# we can import it using "dot notation".

# Starting in the same package that this module lives
    # (the file `app/main.py`) 
# in (the directory `app`/)...
    # look for the subpackage routers 
        # (the directory at `app/routers/`)...
    # and from it, import the submodule `items` 
        # (the file at `app/routers/items.py`)
    # and `users` 
        # (the file at `app/routers/users.py`)...
    # The module `items` will have a variable `router` 
        # (`items.router`). 
        # This is the same one we created in the file `app/routers/items.py`. 
    # It's an APIRouter. The same for the module users.

# We could also (absolute) import them like:
    # `from app.routers import items, users`

app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

## Include an `APIRouter`

# add an APIRouter to the main FastAPI application.
# It will include all the routes from that router as part of it.
app.include_router(
        # Technical Details
            # It will actually internally create a path operation 
            # for each path operation that was declared in the APIRouter.
            # So, behind the scenes, 
                # it will actually work as if everything was the same single app
        
        # Check
            # You don't have to worry about performance when including routers.
                # This will take microseconds 
                # and will only happen at startup.
                # So it won't affect performance
            
        
        users.router
        # imported modules directly 
            # in order to namespace `router` variable 
            # and avoid namespace collisions
        )

## Include an APIRouter with a `prefix`, `tags`, `responses`, and `dependencies`

# these will be added to all path operations in the router
# i.e. union over fields
app.include_router(
        items.router,
        
        prefix="/items",
        # As the path of each path operation has to start with `/`
        # the prefix must NOT include a final `/`.
        
        tags=["items"],
        # These "tags" are especially useful for the 
        # automatic interactive documentation systems (using OpenAPI).

        dependencies=[Depends(get_token_header)],
        # will be executed/solved for each request made to them. 
        # Note
            # much like dependencies in path operation decorators, 
            # NO VALUE WILL BE PASSED TO YOUR PATH OPERATION FUNCTION.
        
        # Tip
            # Having dependencies in a decorator can be used, for example, 
            # to require authentication for a whole group of path operations. 
            # Even if the dependencies are not added individually to each one of them.

        # Dependency call priority:
            # router dependencies are executed first, 
            # then the dependencies in the decorator, 
            # and then the normal parameter dependencies.
        # You can also add Security dependencies with scopes.
        
        responses={404: {"description": "Not found"}},
        # And we can add predefined responses too
        )


## Include the same router multiple times with different prefix
    # You can also use `.include_router()` multiple times 
    # with the same router using different prefixes.
    
    # This could be useful, for example, 
        # to expose the same API under different prefixes, 
            # e.g. `/api/v1` and `/api/latest`.
    # This is an advanced usage that you might not really need, 
    # but it's there in case you do.


# Tip
    # You could also add path operations directly, 
        # for example with: `@app.get(...)`.
    # Apart from `app.include_router()`, in the same FastAPI app.
    # It would still work the same.
        
# Very Technical Details
    # The APIRouters are not "mounted", 
        # they are not isolated from the rest of the application.
    # This is because we want to include their path operations in 
        # the OpenAPI schema and the user interfaces.
    # As we cannot just isolate them and "mount" them independently of the rest,
        # the path operations are "cloned" (re-created), 
        # not included directly.

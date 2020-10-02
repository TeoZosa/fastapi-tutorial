"""Bigger Applications - Multiple Files"""
# If you are building an application or a web API, 
    # it's rarely the case that you can put everything on a single file.
# FastAPI provides a convenience tool to structure your application 
    # while keeping all the flexibility.

 
# Info
    # If you come from Flask, this would be the equivalent of Flask's `Blueprints`.

## An example file structure¶
# Let's say you have a file structure like this:
# .
# ├── app
# │   ├── __init__.py
# │   ├── main.py
# │   └── routers
# │       ├── __init__.py
# │       ├── items.py
# │       └── users.py

## Tip
    # There are two `__init__.py` files: one in each directory or subdirectory.
        # This is what allows importing code from one file into another.
        # For example, in `app/main.py` you could have a line like:
            # `from app.routers import items`

# The `app` directory contains everything.
# This `app` directory has an empty file `app/__init__.py`.
    # So, the `app` directory is a "Python PACKAGE" 
        # (a collection of "Python modules").
# The `app` directory also has a `app/main.py` file.
    # As it is inside a Python package directory 
        # (because there's a file `__init__.py`), 
    # it is a "module" of that PACKAGE: `app.main`.
    
# There's a subdirectory `app/routers/`.
# The subdirectory `app/routers` also has an empty file `__init__.py`.
    # So, it is a "Python SUBPACKAGE".
# The file `app/routers/items.py` is beside the `app/routers/__init__.py`.
    # So, it's a SUBMODULE: `app.routers.items`.
# The file `app/routers/users.py` is beside the `app/routers/__init__.py`.
    # So, it's a SUBMODULE: `app.routers.users`.

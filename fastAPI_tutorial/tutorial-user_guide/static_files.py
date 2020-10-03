"""Static Files"""
# "Mount" a StaticFiles() instance in a specific path.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# All these parameters can be different than "static", 
# adjust them with the needs and specific details of your own application.
app.mount(
        "/static", 
        #  The sub-path this "sub-application" will be "mounted" on. 
        #  So, any path that starts with "/static" will be handled by it.
        
        StaticFiles(directory="static"), 
        # the name of the directory that contains your static files
        
        name="static"
        # a name that can be used internally by FastAPI
        )

# What is "Mounting"
    # Adding a complete "independent" application 
        # in a specific path, 
    # that then takes care of handling all the sub-paths.
    
    # This is different from using an APIRouter 
        # as a mounted application is completely independent. 
    # The OpenAPI and docs from your main application 
    # won't include anything from the mounted application, etc.
    
    # You can read more about this in the Advanced User Guide.

# More info
    # For more details and options check Starlette's docs about Static Files.

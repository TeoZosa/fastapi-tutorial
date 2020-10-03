"""Metadata and Docs URLs"""
# You can customize several metadata configurations in your FastAPI application.

from fastapi import FastAPI

# Tip
    # You don't have to add metadata for all the tags that you use
tags_metadata = [
        
        ## Order of tags
            # The order of each tag metadata dictionary 
            # also defines the order shown in the docs UI.
            # For example, even though users would go after items in alphabetical order, 
            # it is shown before them, 
                # because we added their metadata as the first dictionary in the list.
                
        
        # one dictionary for each tag.
        {
                "name": #REQUIRED 
                    "users",
                # `str` with the same tag name you use in the `tags` parameter 
                # in your path operations and APIRouters.
                
                "description": "Operations with users. The **login** logic is also here.",
                # `str` with a short description for the tag. 
                # It can have Markdown and will be shown in the docs UI.
                },

        # one dictionary for each tag.
        {
                "name": "items",
                "description": "Manage items. So _fancy_ they have their own docs.",
                
                "externalDocs": # dict describing external documentation 
                    {
                        "description": "Items external docs",
                        # `str` with a short description for the external docs.
                            
                        "url": #REQUIRED 
                            "https://fastapi.tiangolo.com/",
                        # `str` with the URL for the external documentation
                            
                        },
                },
        
        
        ]


app = FastAPI(
        # Include below in OpenAPI and the automatic API docs UIs.
        
        ## Title, description, and version
        title="My Super Project",
        description="This is a very fancy project, with auto docs for the API and everything",
        version="2.5.0",
        # Useful for example if you had a previous version of the application, also using OpenAPI.
        
        ## Metadata for tags
        openapi_tags=tags_metadata,
        
        ## OpenAPI URL
        openapi_url="/api/v1/openapi.json", #default: `/openapi.json`
        # to disable the OpenAPI schema completely 
            # you can set `openapi_url=None`, 
            # that will also disable the documentation user interfaces that use it.
        
        ## Docs URLs
        # configure doc serving endpoints
        
        #Swagger UI
        docs_url="/docs",
        #  disable it by setting `docs_url=None`
        
        #ReDoc UI
        redoc_url="/redoc"
        #  disable it by setting `redoc_url=None`
        )

@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]

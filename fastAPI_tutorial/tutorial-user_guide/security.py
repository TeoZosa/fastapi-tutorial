
"""Security Intro"""
# There are many ways to handle security, authentication and authorization.
# And it normally is a complex and "difficult" topic.

# In many frameworks and systems just handling security and authentication 
# takes a big amount of effort and code (in many cases it can be 50% or more
# of all the code written).

# FastAPI provides several tools to help you deal with Security easily, 
# rapidly, in a standard way, without having to study and learn all the 
# security specifications.

# OAuth2
# a specification that defines several ways to handle authentication and authorization.
# It is quite an extensive specification 
#   and covers several complex use cases.
# It includes ways to authenticate using a "third party".
# That's what all the systems with 
# "login with Facebook, Google, Twitter, GitHub" use underneath.
# OAuth2 doesn't specify how to encrypt the communication, 
#   it expects you to have your application served with HTTPS.

# Tip
# In the section about deployment you will see how to set up HTTPS for free,
# using `Traefik` and `Let's Encrypt`.

# OAuth 1 ** It is not very popular or used nowadays**
# There was an OAuth 1, which is very different from OAuth2, and more 
# complex, as it included directly specifications on how to encrypt the 
# communication.

# OpenID Connect
# Based on OAuth2.
# extends OAuth2 specifying some things that are relatively ambiguous in
# OAuth2, to try to make it more interoperable.

# For example, Google login uses OpenID Connect (which underneath uses OAuth2).
# But Facebook login doesn't support OpenID Connect. It has its own flavor 
# of OAuth2.

# OpenID ( NOT"OpenID Connect") ** It is not very popular or used nowadays**
# tried to solve the same thing as OpenID Connect, 
# but was not based on OAuth2.
# So, it was a complete additional system.


## OpenAPI
# (previously known as Swagger) 
# the open specification for building APIs 
# (now part of the Linux Foundation).
# FastAPI is based on OpenAPI.
# That's what makes it possible to have multiple automatic interactive 
# documentation interfaces, code generation, etc.
# OpenAPI has a way to define multiple security "schemes".
# By using them, you can take advantage of all these standard-based tools, 
# including these interactive documentation systems.
# OpenAPI defines the following security schemes:
# `apiKey`: an application specific key that can come from:
# A query parameter.
# A header.
# A cookie.
# `http`: standard HTTP authentication systems, including:
# `bearer`: a header `Authorization` with a value of `Bearer` plus a token. 
# This is inherited from OAuth2.
# HTTP Basic authentication.
# HTTP Digest, etc.
# `oauth2`: all the OAuth2 ways to handle security (called "flows").
# Several of these flows are appropriate for building an OAuth 2.0 
# authentication provider (like Google, Facebook, Twitter, GitHub, etc):
# `implicit`
# `clientCredentials`
# `authorizationCode`
# But there is one specific "flow" 
#   that can be perfectly used for handling 
#   authentication in the same application directly:
# `password`: some next chapters will cover examples of this.
# `openIdConnect`: has a way to define how to discover  
#                  OAuth2 authentication data automatically.
# This automatic discovery is what is defined in the OpenID Connect specification.
# Tip
# Integrating other authentication/authorization providers 
# like Google, Facebook, Twitter, GitHub, etc. 
# is also possible and relatively easy.

# The most complex problem is building an 
# authentication/authorization provider like those, 
# but FastAPI gives you the tools to do it easily, 
# while doing the heavy lifting for you.

## FastAPI utilities
# FastAPI provides several tools for each of these security schemes in the 
# `fastapi.security` module that simplify using these security mechanisms.

# In the next chapters you will see how to add security 
# to your API using those tools provided by FastAPI.

# And you will also see how it gets automatically 
# integrated into the interactive documentation system.

"""Security - First Steps"""
## FastAPI's OAuth2PasswordBearer
# Let's imagine that you have your backend API in some domain.

# And you have a frontend in another domain or in a different path of the 
# same domain (or in a mobile application).

# And you want to have a way for the frontend to authenticate with the 
# backend, using a username and password.

# We can use OAuth2 to build that with FastAPI.

# But let's save you the time of reading the full long specification just to
# find those little pieces of information you need.

# Let's use the tools provided by FastAPI to handle security.
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
# Info
# A "bearer" token is not the only option.
# But it's the best one for our use case.
# And it might be the best for most use cases, 
# unless you are an OAuth2 expert 
# and know exactly why there's another option 
# that suits better your needs.
# In that case, FastAPI also provides you with the tools to build it.

app = FastAPI()

# A callable with signature `oauth2_scheme(some, parameters)` 
oauth2_scheme = OAuth2PasswordBearer(
        # When we create an instance of the OAuth2PasswordBearer class 
        # we pass in the `tokenUrl` parameter. 
        # This parameter contains the URL that the client 
        # (the frontend running in the user's browser) 
        # will use to send the username and password 
        # in order to get a token.
        tokenUrl="token"
        # Tip
        # here `tokenUrl="token"` 
        # refers to a relative URL token that we haven't created yet. 
        # As it's a relative URL, it's equivalent to `./token`
        # Because we are using a relative URL, 
        # if your API was located at 
        # https://example.com/, then it would refer to 
        # https://example.com/token. But if your API was located at 
        # https://example.com/api/v1/, then it would refer to 
        # https://example.com/api/v1/token.
        # Using a relative URL is important 
        # to make sure your application keeps working 
        # even in an advanced use case like Behind a Proxy.
        # Info
        # If you are a very strict "Pythonista" 
        # you might dislike the style of the parameter name 
        # `tokenUrl` instead of `token_url`.
        # That's because it is using the same name as in the OpenAPI spec. 
        # So that if you need to investigate more about 
        # any of these security schemes you can just 
        # copy and paste it to find more information about it.
        )


@app.get("/items/")
async def read_items(token: str =

                     Depends(oauth2_scheme)
                     # This dependency will provide a `str` that is assigned 
                     # to the parameter `token` of the path operation function.

                     # FastAPI will know that it can use this dependency to 
                     # define a "security scheme" in the OpenAPI schema (and
                     # the automatic API docs).

                     # Technical Details
                     # FastAPI will know that it can use the class 
                     # `OAuth2PasswordBearer` (declared in a dependency) 
                     # to define the security scheme in OpenAPI because it 
                     # inherits from 
                     # `fastapi.security.oauth2.OAuth2`, 
                     # which in turn inherits from 
                     # `fastapi.security.base.SecurityBase`.

                     # All the security utilities that integrate with 
                     # OpenAPI (and the automatic API docs) inherit from 
                     # `SecurityBase`, that's how FastAPI can know how to 
                     # integrate them in OpenAPI.
                     ):
    return {"token": token}

# Go to the interactive docs at: http://127.0.0.1:8000/docs
# Authorize button!
# You already have a shiny new "Authorize" button.
# And your path operation has a little lock in the top-right corner that you can click.
# Note
# It doesn't matter what you type in the form, it won't work yet. 
# But we'll get there.
# This is of course not the frontend for the final users, 
# but it's a great automatic tool to document interactively all your API.
# It can be used by the frontend team (that can also be yourself).
# It can be used by third party applications and systems.
# And it can also be used by yourself, 
# to debug, check and test the same application.

##What it does
# It will go and 
# look in the request for that `Authorization` header, 
# check if the value is `Bearer` plus some token, and will  
# return the token as a `str`.

# If it doesn't see an `Authorization` header, 
# or the value doesn't have a `Bearer` token, 
# it will respond with a 401 status code error (`UNAUTHORIZED`) directly.

# You don't even have to check if the token exists to return an error. 
# You can be sure that 
# if your function is executed, 
# it will have a `str` in that token.

# Note:
# We are not verifying the validity of the token yet, 
# but that's a start already.

"""Get Current User"""
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def fake_decode_token(token):
    return User(
            username=token + "fakedecoded",
            email="john@example.com",
            full_name="John Doe"
            )


async def get_current_user(
        # Inject the token 
        token: str = Depends(oauth2_scheme)):
    # Create a Pydantic model (`User`) using the injected token
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(
       
        # Inject the current user
        current_user: User = Depends(get_current_user)
        # Note:
        # Powerful <= this pattern can be used anywhere this dependency is required 
        
        ):
    return current_user
# Note: 
    # The way this dependency system is designed allows us to have different 
    # dependencies (different "dependables") that all return a User model.
    # We are not restricted to having only one dependency that can return that 
    # type of data.

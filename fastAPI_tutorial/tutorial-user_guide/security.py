
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
    
"""Simple OAuth2 with Password and Bearer"""
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# `OAuth2PasswordRequestForm` is a class dependency that declares a form body 
# with:
    # The `username`.
    # The `password`.
    
    # An (optional) `scope` field 
        # as a big string, composed of strings separated by spaces.
        # Tip
            # The instance of the dependency class `OAuth2PasswordRequestForm` 
                # won't have an attribute scope with the long string separated by spaces,
                # instead, it will have a `scopes` attribute 
                    # with the actual list of strings for each scope sent.
            # We are not using scopes in this example, 
            # but the functionality is there if you need it.
            
    # An (optional) `grant_type`.
    # An (optional) `client_id` (we don't need it for our example).
    # An (optional) `client_secret` (we don't need it for our example).
# Tip
    # The OAuth2 spec actually 
        # requires a field `grant_type` 
        # with a fixed value of `password`, 
        # but OAuth2PasswordRequestForm doesn't enforce it.
    # If you need to enforce it, 
        # use `OAuth2PasswordRequestFormStrict` 
        # instead of `OAuth2PasswordRequestForm`.
# Info
    # The `OAuth2PasswordRequestForm` is 
        # NOT A SPECIAL CLASS FOR FASTAPI as is `OAuth2PasswordBearer`.
    # `OAuth2PasswordBearer` 
        # makes FastAPI know that it is a security scheme. 
        # So it is added that way to OpenAPI.
    # But `OAuth2PasswordRequestForm` is 
        # JUST A CLASS DEPENDENCY THAT YOU COULD HAVE WRITTEN YOURSELF, 
        # OR YOU COULD HAVE DECLARED `Form` PARAMETERS DIRECTLY.
        # But as it's a common use case, 
            # it is provided by FastAPI directly, just to make it easier.
            
from pydantic import BaseModel

fake_users_db = {
        "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "fakehashedsecret",
                "disabled": False,
                },
        "alice": {
                "username": "alice",
                "full_name": "Alice Wonderson",
                "email": "alice@example.com",
                "hashed_password": "fakehashedsecret2",
                "disabled": True,
                },
        }

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Now, get the user data from the (fake) database, 
    # using the username from the form field.
    user = fake_decode_token(token)
    if not user:
        # If there is no such user, we return an error saying 
        # "incorrect username or password".
        # For the error, we use the exception `HTTPException`:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
                # Info
                # The additional header 
                    # `WWW-Authenticate` with value `Bearer` 
                # we are returning here is also part of the spec.
                
                # Any HTTP (error) *status code 401 "UNAUTHORIZED" is 
                # supposed to also return a `WWW-Authenticate` header.*
                
                # In the case of bearer tokens (our case), 
                # the value of that header should be `Bearer`.
                    # You can actually skip that extra header and it would still work.
                    # But it's provided here to be compliant with the specifications.
                    # Also, THERE MIGHT BE TOOLS THAT EXPECT AND USE IT 
                    #   (now or in the future) and that 
                    #   might be useful for you or your users, now or in the future. 
                      # That's the benefit of standards...
                )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled: # get the current_user ONLY if this user is active.
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends()
        # OAuth2 specifies that when using the 
        # "password flow" (that we are using) 
        # the CLIENT/USER MUST SEND
        # `username` and `password` fields 
        # as FORM DATA (so, no JSON here).
                ):
    
    user_dict = fake_users_db.get(
            form_data.username
            # And the SPEC SAYS THAT THE FIELDS HAVE TO BE NAMED LIKE THAT. 
            # So `user-name` or `email` wouldn't work.
                # But don't worry, you can show it as you wish to your final users in the frontend.
                # And your database models can use any other names you want.
                # But for the login path operation, we need to use these names to be
                #   compatible with the spec (and be able to, for example, use the 
                #   integrated API documentation system).
            )
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    
    ## Check the password
        ## Password hashing
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    ## Return the token
        # The response of the token endpoint must be a JSON object. It should have a 
            # `token_type`. 
                # In our case, as we are using "Bearer" tokens, 
                # the token type should be "bearer".
            # `access_token`, 
                # with a string containing our access token.
        # For this simple example, we are going to just be 
        # completely insecure and return the same username as the token.
    return {"access_token": user.username, "token_type": "bearer"}
# Tip
    # By the spec, you should return a `JSON` object 
    # with an `access_token` and a `token_type`, the same as in this example.
    # This is something that 
        # YOU HAVE TO DO YOURSELF IN YOUR CODE, and 
        # MAKE SURE YOU USE THOSE specific `JSON` KEYS.
        # It's almost the only thing that you have to remember to do correctly 
        # yourself, to be compliant with the specifications.
    # For the rest, FastAPI handles it for you.

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
    # So, in our endpoint, we will only get a user if 
        # was correctly authenticated, 
            # `login`
                # `hashed_password = fake_hash_password(form_data.password)`
                # if not hashed_password == user.hashed_password:
        # the user exists, 
            # `login` 
                # `user_dict = fake_users_db.get(form_data.username)` 
                # `if not user_dict:`
            # `get_current_user`
                # `user = fake_decode_token(token)` 
                # `if not user:`
        # and is active 
            # `get_current_active_user`
                # `if current_user.disabled:`

# Tip
    # In the next chapter, you will see a real secure implementation, 
    # with password hashing and JWT tokens.
    # But for now, let's focus on the specific details we need.

"""OAuth2 with Password (and hashing), Bearer with JWT tokens"""
## About JWT
# JWT means "JSON Web Tokens".
# 
# It's a standard to codify a JSON object 
# in a long dense string without spaces. It looks like this:
    # `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`
    
# It is NOT ENCRYPTED, so, 
    # anyone could recover the information from the contents.
# But it's signed. 
    # So, when you receive a token that you emitted, 
    # you can verify that you actually emitted it.
# That way, you can create a token with an expiration 
    # of, let's say, 1 week.
        # And then when the user comes back the next day with the token, 
        # you know that user is still logged in to your system.
    # After a week, 
        # the token will be expired 
        # and the user will not be authorized 
        # and will have to sign in again to get a new token. 
        # And if the user (or a third party) tried to modify the token to change the expiration, 
            # you would be able to discover it, 
            # because the signatures would not match.
# If you want to play with JWT tokens and see how they work, 
# check https://jwt.io.

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from passlib.context import CryptContext
# Tip
    # With passlib, you could even configure it to be able to read passwords created by 
        # Django, 
        # a Flask security plug-in 
        # or many others.
    # So, you would be able to, for example, 
        # share the same data from a 
            # Django application in a database with a FastAPI application. 
        # Or gradually migrate a Django application using the same database.
    # And your users would be able to login 
        # from your Django app 
        # or from your FastAPI app, at the same time.
# Tip
    # The PassLib context also has functionality to use 
        # different hashing algorithms, 
        # including deprecated old ones only to allow verifying them, etc.
    # For example, you could use it 
        # to read and verify passwords generated by another system (like Django) 
        # but hash any new passwords with a different algorithm like Bcrypt.
        # And be compatible with all of them at the same time.
from pydantic import BaseModel

# Key/Algorithm to sign JWT token
# random secret key
SECRET_KEY = "0e954d098c02451610e9f5150930ed6ce7b431711358b25b0db471eeecf807d3"
# to get a string like this run:
# `openssl rand -hex 32`
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
        "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "disabled": False,
                }
        }

# Define a Pydantic Model that will be used in the token endpoint for the response.
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# And another utility to verify if a received password matches the hash stored.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create a utility function to hash a password coming from the user.
def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# And another one to authenticate and return a user.
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Create a utility function to generate a new access token.
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# receive the same token as before, but this time, using JWT tokens.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
    # Decode the received token, verify it, and return the current user.
    try:
        # Decode the received token, verify it
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        # If the token is invalid, return an HTTP error right away.
        raise credentials_exception
    
    # return the current user.
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
                )
    # Create a timedelta with the expiration time of the token.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create a real JWT access token and return it.
    access_token = create_access_token(
            data={"sub": user.username}, 
            ## Technical details about the JWT "subject" sub
                # The JWT specification says that there's 
                    # a key `sub`, with the subject of the token.
                    # It's optional to use it, 
                        # but that's where you would put the user's identification, 
                        # so we are using it here.
            
                # JWT might be used for other things apart from identifying a 
                # user and allowing them to perform operations directly on your API.
                    # For example, you could identify a "car" or a "blog post".
                        # Then you could add permissions about that entity, 
                            # like "drive" (for the car) 
                            # or "edit" (for the blog).
                        # And then, you could give that JWT token to a user (or bot), 
                            # and they could use it to perform those actions 
                                # (drive the car, or edit the blog post) 
                            # without even needing to have an account, 
                            # just with the JWT token your API generated for that.
                    # Using these ideas, JWT can be used for way more sophisticated scenarios.
            
                # In those cases, several of those entities could have the same ID,
                    # let's say `foo` (a user `foo`, a car `foo`, and a blog post `foo`).
                # So, to avoid ID collisions, 
                    # when creating the JWT token for the user, 
                        # you could prefix the value of the `sub` key, e.g. with `username` 
                        # So, in this example, the value of `sub` could have been: 
                            # `username:johndoe`
            
                # The important thing to have in mind is that the `sub` key should 
                    # HAVE A UNIQUE IDENTIFIER ACROSS THE ENTIRE APPLICATION, 
                    # and it SHOULD BE A STRING.
                    
            expires_delta=access_token_expires
            )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

# Authorize the application the same way as before. Using the credentials:
    # Username: johndoe 
    # Password: secret
# If you open the developer tools, you could see 
    # how the data sent 
    # and only includes the token, 
# the password is only sent in the 
    # first request to authenticate the user and get that access token, 
    # but not afterwards
    # i.e., `Form data` in `Headers` of `token` request resource
    # => introspectable with plaintext (all password flows in general)

## Advanced usage with `scopes`
    # OAuth2 has the notion of "scopes".
        # You can use them to add a specific set of permissions to a JWT token.
        # Then you can give this token to a user directly or a third party, 
            # to interact with your API with a set of restrictions.
        
    # You can learn more in the Advanced User Guide about how to 
        # use OAuth2 "scopes", 
            # for a more fine-grained permission system, 
            # following these same standards. 
        # OAuth2 with scopes is the mechanism used by many big authentication providers, 
            # like Facebook, Google, GitHub, Microsoft, Twitter, etc. 
        # to authorize third party applications to interact with their APIs on behalf of their users.

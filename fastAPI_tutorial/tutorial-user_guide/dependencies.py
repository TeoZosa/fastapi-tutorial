"""Dependencies - First Steps"""
## What is "Dependency Injection"
# "Dependency Injection" means, in programming, 
#   that there is a way for your code 
#   (in this case, your path operation functions) 
#   to declare things that it requires to work and use: "dependencies".

# And then, that system (in this case FastAPI) 
#   will take care of doing whatever is needed to provide your code 
#   with those needed dependencies ("inject" the dependencies).

# This is very useful when you need to:
# Have shared logic (the same code logic again and again).
# Share database connections.
# Enforce security, authentication, role requirements, etc.
# And many other things...
# All these, while minimizing code repetition.

# Other common terms for this same idea of "dependency injection" are:
# resources
# providers
# services
# injectables
# components

from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()

# Create a dependency, or "dependable"
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(
        # Declare the dependency, in the "dependant"
        # The same way you use `Body`, `Query`, etc. with your path operation function parameters, 
        # use `Depends` with a new parameter
        commons: dict = Depends(common_parameters)
        # Note: `Depends` accepts any callable, not just fns
        ):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

## FastAPI compatibility
# The simplicity of the dependency injection system 
#   makes FastAPI compatible with:
# all the relational databases
# NoSQL databases
# external packages
# external APIs
# authentication and authorization systems
# API usage monitoring systems
# response data injection systems
# etc.

## Simple and Powerful
# You can define dependencies 
# that in turn can define dependencies themselves.
# In the end, a hierarchical tree of dependencies is built, 
# and the Dependency Injection system takes care of 
# solving all these dependencies for you (and their sub-dependencies) 
# and providing (injecting) the results at each step.

## Integrated with OpenAPI
# All these dependencies, while declaring their requirements, also add 
# parameters, validations, etc. to your path operations.
# FastAPI will take care of adding it all to the OpenAPI schema, 
# so that it is shown in the interactive documentation systems.

"""Classes as Dependencies"""
from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(
        # Infer the callable from the `CommonQueryParams` type annotation 
        # (since `CommonQueryParams` is a class) 
        commons: CommonQueryParams = Depends(),
        # ==
        # commons: CommonQueryParams = Depends(CommonQueryParams),

        # Note: 
        # If shorthand seems more confusing than helpful, 
        #   disregard it, you don't need it. It is just a shortcut. 

        ):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

"""Sub-dependencies"""
from typing import Optional

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()

# First dependency 
# "dependable"
def query_extractor(q: Optional[str] = None):
    return q

# Second dependency, 
# "dependable" AND "dependant"
def query_or_cookie_extractor(
        q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
        ):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
        # Use the dependency
        query_or_default: str = Depends(query_or_cookie_extractor)
        # Notice that we are 
        # only declaring one dependency in the path operation function, 
        #   the `query_or_cookie_extractor`.
        # But FastAPI will know that it has to solve `query_extractor` first, 
        #   to pass the results of that to `query_or_cookie_extractor` while calling it.
        ):
    return {"q_or_cookie": query_or_default}

## Using the same dependency multiple times

# If one of your dependencies is declared multiple times for the same path operation, 
# for example, multiple dependencies have a common sub-dependency, 
# FastAPI will know to call that sub-dependency only once per request.

# And it will save the returned value in a "cache" 
# and pass it to all the "dependants" that need it in that specific request,
# instead of calling the dependency multiple times for the same request.

def get_value():
    return "VALUE!"

async def needy_dependency(
        fresh_value: str = Depends(get_value,

                                   # In an advanced scenario where you 
                                   # know you need the dependency to be called
                                   # at every step (possibly multiple times) in the same request 
                                   # instead of using the "cached" value 
                                   use_cache=False)):
    return {"fresh_value": fresh_value}
# Tip
# All this might not seem as useful with these simple examples.
# But you will see how useful it is in the chapters about SECURITY.
# And you will also see the amounts of code it will save you.

"""Dependencies in path operation decorators"""
# In some cases you don't really need 
# the return value of a dependency inside your path operation function.
# Or the dependency doesn't return a value.

# But you still need it to be executed/solved.
# For those cases, 
#  instead of declaring a path operation function parameter with `Depends`, 
#  you can add a list of dependencies to the path operation decorator.

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token(
        # Dependency requirements
        # request requirements (like headers) or other sub-dependencies
        x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        # dependencies can raise exceptions, the same as normal dependencies
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    # They can return values or not, the values won't be used.
    return x_key


@app.get("/items/",
         # dependencies will be executed/solved the same way normal dependencies. 
         # But their value (if they return any) 
         # won't be passed to your path operation function.
         dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

## Dependencies for a group of path operations
# Later, when reading about how to structure bigger applications 
# ("Bigger Applications - Multiple Files"), 
# possibly with multiple files,
# you will learn how to declare a single dependencies parameter for a group
# of path operations.

"""Dependencies with yield"""
## Technical Details
# Any function that is valid to use with:
# `@contextlib.contextmanager` or
# `@contextlib.asynccontextmanager`
# would be valid to use as a FastAPI dependency.
# In fact, FastAPI uses those two decorators internally.

class DBSession:
    def close(self, *args):
        pass

async def get_db():
    db = DBSession()
    try:
        # yielded value is what is injected into 
        # path operations and other dependencies
        yield db
    # code following the yield statement 
    # is executed after the response has been delivered

    # use finally to make sure the exit steps are executed, 
    # no matter if there was an exception or not.
    finally:
        db.close()

## Sub-dependencies with yield
# You can have sub-dependencies and "trees" of sub-dependencies 
# of any size and shape, and any or all of them can use yield.

# FastAPI will make sure that the "exit code" 
# in each dependency with yield is run in the correct order.
from fastapi import Depends

def generate_dep_a() -> DBSession:
    return DBSession()

def generate_dep_b() -> DBSession:
    return DBSession()

def generate_dep_c() -> DBSession:
    return DBSession()

async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()

# `dependency_b` can depend on `dependency_a`
async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        # And, in turn, `dependency_b` 
        # needs the value from dependency_a (here named dep_a) to be available for its exit code.
        dep_b.close(dep_a)

# `dependency_c` can depend on `dependency_b`,
async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        # In this case `dependency_c`, to execute its exit code, 
        # needs the value from dependency_b (here named dep_b) to still be available.
        dep_c.close(dep_b)

# The same way, 
# you could have dependencies with yield and return mixed.
# And you could have a single dependency that requires several other dependencies with yield, etc.
# You can have any combinations of dependencies that you want.
# FastAPI will make sure everything is run in the correct order.

# Technical Details
# This works thanks to Python's Context Managers.
# FastAPI uses them internally to achieve this.

## Dependencies with yield and HTTPException

# if you raise an `HTTPException` after the yield, the default (or any custom)
# exception handler that catches `HTTPExceptions` and returns an HTTP 400 response 
# WON'T BE THERE TO CATCH THAT EXCEPTION ANYMORE.

# This is what allows anything set in the dependency 
# (e.g. a DB session) 
# to, for example, be used by background tasks.

# Background tasks are run AFTER THE RESPONSE HAS BEEN SENT. 
# So there's no way to raise an `HTTPException` 
# because there's NOT EVEN A WAY TO CHANGE THE RESPONSE THAT IS ALREADY SENT.

# But if a background task creates a DB error, 
# at least you can rollback or cleanly close the session 
# in the dependency with yield, 
# and maybe log the error or report it to a remote tracking system.

# If you have some code that you know could raise an exception, 
# do the most normal/"Pythonic" thing 
# and add a try block in that section of the code.

# If you have custom exceptions 
# that you would like to handle before returning the response 
# and possibly modifying the response, 
# maybe even raising an HTTPException, 
# create a Custom Exception Handler.

# Can still raise exceptions including HTTPException BEFORE THE YIELD BUT NOT AFTER.

# see [diagram](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#dependencies-with-yield-and-httpexception)

# Info
# Only one response will be sent to the client. It might be one of the error
# responses or it will be the response from the path operation.
# After one of those responses is sent, no other response can be sent.

# Tip
# This diagram shows HTTPException, but you could also raise any other 
# exception for which you create a Custom Exception Handler. And that 
# exception would be handled by that custom exception handler instead of the
# dependency exit code.

# But if you raise an exception that is not handled by the exception 
# handlers, it will be handled by the exit code of the dependency.

## Context Managers
# When you create a dependency with yield, 
# FastAPI will internally convert it to a context manager, 
# and combine it with some other related tools.

# Warning
# This is, more or less, an "advanced" idea.
# If you are just starting with FastAPI you might want to skip it for now.
class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    # ctx mgr req function #1
    def __enter__(self):
        return self.db

    # ctx mgr req function #2
    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    # You can use Context Managers inside of FastAPI dependencies 
    # with `yield` by using `with` or `async with` statements 
    # inside of the dependency function:
    with MySuperContextManager() as db:
        yield db

# Tip
# Another way to create a context manager is with:
# `@contextlib.contextmanager` or
# `@contextlib.asynccontextmanager`
# using them to decorate a function with a single yield.
# That's what FastAPI uses internally for dependencies with yield.

# But you don't have to use the decorators for FastAPI dependencies 
# (AND YOU SHOULDN'T).
# FastAPI will do it for you internally.

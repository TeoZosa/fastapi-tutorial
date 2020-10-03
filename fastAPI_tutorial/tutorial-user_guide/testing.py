"""Testing"""
# Thanks to Starlette, testing FastAPI applications is easy and enjoyable.
# It is based on Requests, so it's very familiar and intuitive.
# With it, you can use pytest directly with FastAPI.

## Using TestClient

from fastapi import FastAPI

# Import TestClient.
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


# Create a `TestClient` passing to it your FastAPI.
client = TestClient(app)

# Create functions with a name that starts with `test_` 
# (this is standard pytest conventions).
def test_read_main():
    # Use the TestClient object the same way as you do with requests.
    response = client.get("/")

    # Write simple assert statements with the standard Python expressions that 
    # you need to check (again, standard pytest).
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# Tip
    # Notice that the testing functions are normal `def`, NOT `async def`.
    # And the calls to the client are also normal calls, NOT using `await`.
    # This allows you to use pytest directly without complications.

# Tip
    # If you want to call async functions in your tests 
    # apart from sending requests to your FastAPI application 
        # (e.g. asynchronous database functions), 
    # have a look at the "Async Tests" in the advanced tutorial.
     
    # Whenever you need the client to pass information in the request 
    # and you don't know how to, 
    # you can search (Google) how to do it in `requests`.
    # Then you just do the same in your tests.
    # E.g.:
        # To pass a path or query parameter, 
            # add it to the URL itself.
        # To pass a JSON body, 
            # pass a Python object (e.g. a dict) to the parameter json.
        # If you need to send Form Data instead of JSON, 
            # use the data parameter instead.
        # To pass headers, 
            # use a dict in the headers parameter.
        # For cookies, 
            # a dict in the cookies parameter.
            
    # For more information about how to pass data to the backend 
        # (using requests or the TestClient) 
    # check the `Requests` documentation.

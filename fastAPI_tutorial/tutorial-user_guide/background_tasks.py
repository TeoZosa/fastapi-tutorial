"""Background Tasks"""
# async operations via background task 

# You can define background tasks to be run after returning a response.
    # useful for operations that need to happen after a request, 
    # but the client doesn't need the operation to complete before receiving the response.

# This includes, for example:
    # Email notifications sent after performing an action:
        # As connecting to an email server and sending an email tends to be "slow" 
            # ( several seconds), 
        # you can return the response right away 
        # and send the email notification in the background.

    # Processing data:
    # let's say you receive a file that must go through a slow process, 
        # you can return a response of "Accepted" (HTTP 202) 
        # and process it in the background.


# In this example, 
    # the messages will be written to the log.txt file after the response is sent.
    # If there was a query in the request, it will be written to the log in a background task.
    # And then another background task generated at the path operation function will write a message using the `email` path parameter.
    
from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()

## Create a task function

# Create a function to be run as the background task.
    # It is just a standard function that can receive parameters.
    # It can be an async def or normal def function, 
        # FastAPI will know how to handle it correctly.
    # And as the write operation doesn't use `async` and `await`, 
        # we define the function with normal `def`

# the messages will be written to the log.txt file after the response is sent.
def write_log(message: str, unused_kwarg=""):
    with open("log.txt", mode="a") as log:
        log.write(message)

# If there was a query in the request, it will be written to the log in a background task.
def get_query(
        # define a parameter in your path operation function 
        # with a type declaration of `BackgroundTasks`
        background_tasks: BackgroundTasks, 
        # FastAPI will create the object of type `BackgroundTasks` for you 
        # and pass it as that parameter.
        
        q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        
    
        background_tasks.add_task(write_log, message)
        # Inside of your path operation function, 
        # pass your task function to the background tasks object 
        # with the method `.add_task()` which receives as arguments:
            # A task function to be run in the background 
                # (`write_log`).
            # Any sequence of arguments 
                # that should be passed to the task function in order 
                # (`message`).
            # Any keyword arguments 
                # that should be passed to the task function (`unused_kwarg="some notification"`)
    return q

# Another background task generated at the path operation 
# function will write a message using the email path parameter.
@app.post("/send-notification/{email}")
async def send_notification(
        email: str,
        background_tasks: BackgroundTasks,
        ## Dependency Injection
            # Using BackgroundTasks also works with the dependency injection system, 
                # you can declare a parameter of type BackgroundTasks at multiple levels: 
                    # in a path operation function, 
                    # in a dependency (dependable), 
                    # in a sub-dependency, 
                    # etc.
            
                # FastAPI knows what to do in each case 
                # and how to re-use the same object, 
                # so that all the background tasks are merged together 
                # and are run in the background afterwards:
        q: str = Depends(get_query)
        ):
    message = f"message to {email}\n"
    
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
    # messages will be written to the log.txt file after the response is sent.

# Technical Details
    # The class `BackgroundTasks` comes directly from `starlette.background`.
    
    # It is imported/included directly into FastAPI so that you can import it from `fastapi` 
    # and avoid accidentally importing the alternative `BackgroundTask` 
        # (WITHOUT THE S AT THE END) 
        # from `starlette.background`.
    
    # By only using `BackgroundTasks` (and NOT `BackgroundTask`), 
        # it's then possible to use it as a path operation function parameter 
        # and have FastAPI handle the rest for you, 
        # just like when using the `Request` object directly.
        
    # It's still possible to use `BackgroundTask` alone in FastAPI, 
        # but you have to create the object in your code 
        # and return a Starlette Response including it.
        # You can see more details in Starlette's official docs for Background Tasks.

# Caveat
    # IF YOU NEED TO PERFORM HEAVY BACKGROUND COMPUTATION 
    # and you don't necessarily need it to be run by the same process 
        # (for example, you don't need to share memory, variables, etc), 
    # YOU MIGHT BENEFIT FROM USING OTHER BIGGER TOOLS 
        # e.g., Celery.
    
    # They tend to require 
        # more complex configurations, 
        # a message/job queue manager, 
            # like RabbitMQ or Redis, 
    
    # but they allow you to run background tasks in multiple processes, 
        # and especially, in multiple servers.
    
    # To see an example, check the "Project Generators", 
        # they all include Celery already configured.
    
    # But if you need to access variables and objects from the same FastAPI app,
    # or you need to perform small background tasks 
        # (like sending an email notification), 
    # you can simply just use `BackgroundTasks`.

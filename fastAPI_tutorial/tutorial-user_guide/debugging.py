"""Debugging"""
# You can connect the debugger in your editor, 
# for example with Visual Studio Code or PyCharm.

# In your FastAPI application, import and run uvicorn directly:
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # Because you are running the Uvicorn server directly from your code, 
    # you can call your Python program (your FastAPI application) 
    # directly from the debugger.

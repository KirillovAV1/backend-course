from fastapi import FastAPI

app = FastAPI()

@app.get("/hotels")
def func():
    return "Hello World"
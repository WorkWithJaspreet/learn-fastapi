from fastapi import FastAPI

app = FastAPI()


# Path operation
@app.get("/")  # Path operation decorator with the path and operation type
async def root():  # Path operation function
    return {"message": "Hello World"}

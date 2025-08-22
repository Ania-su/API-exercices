from typing import List
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse

app = FastAPI()

class User(BaseModel):
    id : int
    name : str
    email : str

post_users :List[User] = [
    User(id=1, name="Ania", email="ania@example.com"),
    User(id=2, name="Williest", email="williest@example.com"),
]

@app.get("/ping")
def hello():
    return Response(content="pong", status_code=200, media_type="text/plain")

@app.get("/users")
async def get_users( page : int = Query(1, ge=1), size : int = Query(20, ge=1, le=100)):
    try:
        start = (page - 1) * size
        end = start + size
        return {"users": post_users[start:end]}
    except Exception:
        raise HTTPException(status_code=400, detail={"error": "Bad types for provided query parameters"})
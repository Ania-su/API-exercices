from typing import List
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse

app = FastAPI()

#User (exo 2)
class User(BaseModel):
    id : int
    name : str
    email : str

post_users :List[User] = [
    User(id=1, name="Ania", email="ania@example.com"),
    User(id=2, name="Williest", email="williest@example.com"),
]

#Task (exo 3)
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks: List[Task] = [
    Task(id=1, title="Faire le lit", completed=True),
    Task(id=2, title="Faire le dîner", completed=False),
]

#Exo1
@app.get("/ping")
def hello():
    return Response(content="pong", status_code=200, media_type="text/plain")

#Exo2
@app.get("/users")
async def get_users( page : int = Query(1, ge=1), size : int = Query(20, ge=1, le=100)):
    try:
        start = (page - 1) * size
        end = start + size
        return {"users": post_users[start:end]}
    except Exception:
        raise HTTPException(status_code=400, detail={"error": "Bad types for provided query parameters"})

#Exo 3
@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks", status_code=201)
def create_tasks(new_tasks: List[Task]):
    tasks.extend(new_tasks)
    return new_tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
def delete_task(id: int):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks")
def delete_tasks(ids: List[int]):
    deleted = []
    for task in tasks[:]:
        if task.id in ids:
            tasks.remove(task)
            deleted.append(task)
    return deleted

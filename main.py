from fastapi import FastAPI
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    priority: int = Field(default=0, ge=0, le=5)     

class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    done: bool | None = None

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

tasks: dict[int, Task] = {}
next_id = 1

@app.post("/tasks", response_model=Task)
def create_task(payload: TaskCreate):
    global next_id

    task = Task(
        id=next_id,
        title=payload.title,
        description=payload.description,
        done=False,
    )
    tasks[task.id] = task
    next_id += 1
    return task

    

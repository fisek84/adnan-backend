from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from notion_service import get_goals, get_tasks, update_goal_status, update_task_status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "OK", "message": "AdnanAI backend radi."}

@app.get("/goals")
def list_goals():
    return get_goals()

@app.get("/tasks")
def list_tasks():
    return get_tasks()

@app.post("/goals/{page_id}/{status}")
def update_goal(page_id: str, status: str):
    return update_goal_status(page_id, status)

@app.post("/tasks/{page_id}/{status}")
def update_task(page_id: str, status: str):
    return update_task_status(page_id, status)

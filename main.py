from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from notion_client import Client
import os
from dotenv import load_dotenv

# ----------------------------
# LOAD ENV VARS
# ----------------------------
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
GOALS_DB_ID = os.getenv("GOALS_DB_ID")
TASKS_DB_ID = os.getenv("TASKS_DB_ID")

notion = Client(auth=NOTION_TOKEN)
app = FastAPI()

# ----------------------------
# PYDANTIC MODELS
# ----------------------------

class GoalCreate(BaseModel):
    name: Optional[str] = None
    outcome_state: Optional[str] = None
    outcome_result: Optional[str] = None
    activity_state: Optional[str] = None
    context_state: Optional[str] = None

class TaskCreate(BaseModel):
    name: str
    goal_id: Optional[str] = None  # optional relation to a goal

# ----------------------------
# HELPER: NAME GENERATOR
# ----------------------------

def generate_goal_name(data: GoalCreate):
    # A) Ako name postoji → koristi ga
    if data.name:
        return data.name

    # B) Ako nema name → koristi drugo polje redom
    if data.outcome_state:
        return f"Goal: {data.outcome_state}"
    if data.outcome_result:
        return f"Goal: {data.outcome_result}"
    if data.activity_state:
        return f"Goal: {data.activity_state}"
    if data.context_state:
        return f"Goal: {data.context_state}"

    # C) Ako ništa ne postoji → error
    return None

# ----------------------------
# ROOT
# ----------------------------

@app.get("/")
def root():
    return {"status": "OK", "message": "AdnanAI backend radi."}

# ----------------------------
# GET GOALS
# ----------------------------

@app.get("/goals")
def get_goals():
    try:
        result = notion.databases.query(database_id=GOALS_DB_ID)
        return result
    except Exception as e:
        return {"error": str(e)}

# ----------------------------
# GET TASKS
# ----------------------------

@app.get("/tasks")
def get_tasks():
    try:
        result = notion.databases.query(database_id=TASKS_DB_ID)
        return result
    except Exception as e:
        return {"error": str(e)}

# ----------------------------
# POST GOALS (NEW)
# ----------------------------

@app.post("/goals")
def create_goal(data: GoalCreate):

    # 1. GENERIŠI IME
    generated_name = generate_goal_name(data)
    if not generated_name:
        return {"error": "Name is missing"}

    # 2. MAPIRAJ PROPERTIES
    properties = {
        "Name": {
            "title": [{"text": {"content": generated_name}}]
        }
    }

    if data.outcome_state:
        properties["Outcome State"] = {"select": {"name": data.outcome_state}}

    if data.outcome_result:
        properties["Outcome Result"] = {"rich_text": [{"text": {"content": data.outcome_result}}]}

    if data.activity_state:
        properties["Activity State"] = {"select": {"name": data.activity_state}}

    if data.context_state:
        properties["Context State"] = {"select": {"name": data.context_state}}

    # 3. CREATE PAGE U NOTION DATABASE
    try:
        result = notion.pages.create(
            parent={"database_id": GOALS_DB_ID},
            properties=properties
        )

        return {
            "status": "success",
            "goal_id": result["id"],
            "name": generated_name
        }

    except Exception as e:
        return {"error": str(e)}

# ----------------------------
# POST TASKS (NEW)
# ----------------------------

@app.post("/tasks")
def create_task(data: TaskCreate):
    if not data.name:
        return {"error": "Task name is required"}

    properties = {
        "Name": {
            "title": [{"text": {"content": data.name}}]
        }
    }

    if data.goal_id:
        properties["Goal"] = {
            "relation": [{"id": data.goal_id}]
        }

    try:
        result = notion.pages.create(
            parent={"database_id": TASKS_DB_ID},
            properties=properties
        )

        return {
            "status": "success",
            "task_id": result["id"],
            "name": data.name,
            "goal_id": data.goal_id
        }

    except Exception as e:
        return {"error": str(e)}

from fastapi import FastAPI
from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
GOALS_DB_ID = os.getenv("GOALS_DB_ID")
TASKS_DB_ID = os.getenv("TASKS_DB_ID")

notion = Client(auth=NOTION_TOKEN)
app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "message": "AdnanAI backend radi."}

@app.get("/goals")
def get_goals():
    try:
        result = notion.databases.query(database_id=GOALS_DB_ID)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/tasks")
def get_tasks():
    try:
        result = notion.databases.query(database_id=TASKS_DB_ID)
        return result
    except Exception as e:
        return {"error": str(e)}

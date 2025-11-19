from notion_client import Client
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
GOALS_DB_ID = os.getenv("GOALS_DB_ID")
TASKS_DB_ID = os.getenv("TASKS_DB_ID")

# Provjeri da li su varijable postavljene
if not NOTION_TOKEN:
    raise ValueError("NOTION_TOKEN is missing from environment variables.")
if not GOALS_DB_ID:
    raise ValueError("GOALS_DB_ID is missing from environment variables.")
if not TASKS_DB_ID:
    raise ValueError("TASKS_DB_ID is missing from environment variables.")

notion = Client(auth=NOTION_TOKEN)

def get_goals():
    try:
        return notion.databases.query_database(database_id=GOALS_DB_ID)
    except Exception as e:
        print(f"Error getting goals: {e}")
        return {"error": str(e)}

def get_tasks():
    try:
        return notion.databases.query_database(database_id=TASKS_DB_ID)
    except Exception as e:
        print(f"Error getting tasks: {e}")
        return {"error": str(e)}

def update_goal_status(page_id, new_status):
    try:
        return notion.pages.update(
            page_id=page_id,
            properties={
                "Goal State": {"select": {"name": new_status}}
            }
        )
    except Exception as e:
        print(f"Error updating goal: {e}")
        return {"error": str(e)}

def update_task_status(page_id, new_status):
    try:
        return notion.pages.update(
            page_id=page_id,
            properties={
                "Task Status": {"select": {"name": new_status}}
            }
        )
    except Exception as e:
        print(f"Error updating task: {e}")
        return {"error": str(e)}

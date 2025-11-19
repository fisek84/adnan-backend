from notion_client import Client
import os

notion = Client(auth=os.getenv("NOTION_TOKEN"))

GOALS_DB_ID = os.getenv("GOALS_DB_ID")
TASKS_DB_ID = os.getenv("TASKS_DB_ID")

def get_goals():
    return notion.databases.query(database_id=GOALS_DB_ID)

def get_tasks():
    return notion.databases.query(database_id=TASKS_DB_ID)

def update_goal_status(page_id, new_status):
    return notion.pages.update(
        page_id=page_id,
        properties={
            "Goal State": {"select": {"name": new_status}}
        }
    )

def update_task_status(page_id, new_status):
    return notion.pages.update(
        page_id=page_id,
        properties={
            "Task Status": {"select": {"name": new_status}}
        }
    )

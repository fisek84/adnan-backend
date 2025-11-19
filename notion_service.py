from notion_client import Client
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
GOALS_DB_ID = os.getenv("GOALS_DB_ID")
TASKS_DB_ID = os.getenv("TASKS_DB_ID")

# Validacija environment varijabli
missing = [name for name, val in {
    "NOTION_TOKEN": NOTION_TOKEN,
    "GOALS_DB_ID": GOALS_DB_ID,
    "TASKS_DB_ID": TASKS_DB_ID
}.items() if not val]
if missing:
    raise ValueError(f"Missing env vars: {', '.join(missing)}")

# Inicijalizacija Notion klijenta
notion = Client(auth=NOTION_TOKEN)

# Dohvati ciljeve
def get_goals():
    try:
        return notion.databases.query(database_id=GOALS_DB_ID)
    except Exception as e:
        return {"error": str(e)}

# Dohvati zadatke
def get_tasks():
    try:
        return notion.databases.query(database_id=TASKS_DB_ID)
    except Exception as e:
        return {"error": str(e)}

# Ažuriraj status cilja
def update_goal_status(page_id, new_status):
    try:
        return notion.pages.update(
            page_id=page_id,
            properties={
                "Goal State": {
                    "select": {"name": new_status}
                }
            }
        )
    except Exception as e:
        return {"error": str(e)}

# Ažuriraj status zadatka
def update_task_status(page_id, new_status):
    try:
        return notion.pages.update(
            page_id=page_id,
            properties={
                "Task Status": {
                    "select": {"name": new_status}
                }
            }
        )
    except Exception as e:
        return {"error": str(e)}

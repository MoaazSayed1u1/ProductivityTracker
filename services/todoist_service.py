from dotenv import load_dotenv
import os
from todoist_api_python.api import TodoistAPI

load_dotenv()

TOKEN = os.getenv("TODOIST_API_TOKEN")

api = TodoistAPI(TOKEN)

def get_tasks():
    try:
        pages = api.get_tasks()

        tasks = []

        for page in pages:
            tasks.extend(page)

        return tasks

    except Exception as e:
        print(e)
        return []

def get_projects():
    try:
        pages = api.get_projects()

        projects = []

        for page in pages:
            projects.extend(page)

        return projects

    except Exception as e:
        print(e)
        return []
    
def get_tasks_by_project(project_id):
    try:
        pages = api.get_tasks(project_id=project_id)

        tasks = []

        for page in pages:
            tasks.extend(page)

        return tasks

    except Exception as e:
        print(e)
        return []

def complete_task(task_id):
    try:
        api.close_task(task_id)
    except Exception as e:
        print(e)